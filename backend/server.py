from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian, auth_required, current_user_id
from flask_cors import CORS
from datetime import datetime
import uuid
import shutil
import os
from weather import get_temperature, get_humidity, get_current_date

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# Add databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# add secret key TODO CHANGE THE KEY
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 5}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['PRAETORIAN_ROLES_DISABLED'] = True
app.config['DEFAULT_ROLES_DISABLED'] = True
# Initalise the database, JWT token libray and CORS
db = SQLAlchemy()
guard = Praetorian()
cors = CORS()


# Create database model (add authentication session token)
class users(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    pfp_id = db.Column(db.Integer)
    remarks = db.Column(db.String(200))

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id
    
    @property # Praetorian library requires roles for tokens even when roles are disabled in config
    def rolenames(self):
        return []


class images(db.Model):
    pid = db.Column(db.String(), primary_key = True)
    id = db.Column("id", db.ForeignKey(users.id))
    prediction = db.Column(db.Integer)
    feedback = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    purchase_date = db.Column(db.DateTime)
    consume_date = db.Column(db.DateTime)
    fruit = db.Column(db.String(20))
    temperature = db.Column(db.Integer)
    humidity =  db.Column(db.Integer)
    consumed = db.Column(db.Boolean)
    alert_day = db.Column(db.Integer)
    data = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<PID %r>' % self.pid

class token_blacklist(db.Model):
    token = db.Column(db.String(400), primary_key = True)
    expiry_date = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<Token %r>' % self.token

    
# Create the database if it does not exist
app.app_context().push()
db.init_app(app)
with app.app_context():
    db.create_all()
# Initialize the flask-praetorian instance for the app
guard.init_app(app, users)
# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)

# Checks if the token has been logged out
def isTokenInBlacklist(token):
    dbToken = token_blacklist.query.get(token)
    if dbToken is None:
        return False
    return True
# Checks if the file is in correct format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# USER FUNCTIONS ----------------------------------------------------------------------------------
@app.route('/register', methods=['POST'])
def user_register():
    """
    Route to create and login new user
    Args:
        email(string): Email of the user
        name(string): Username of the user
        password(string): Password of the user
        passwordconfirmation(string): Repeat of user's password for confirmation

    return: JWT token for authentication
    """
    user_data = request.json
    user_email = user_data.get("email")
    user_name = user_data.get("name")
    user_password = user_data.get("password")
    user_password_confirmation = user_data.get("passwordconfirmation")
    user_id = str(uuid.uuid4())


    # Check if inputted passwords match

    if user_password != user_password_confirmation:
        return "Passwords do not match", 400

    # Check if the email is already in the database
    email_query = users.query.filter_by(email=user_email).first()
    if email_query is not None:
        return "Email is already registered", 409

    # Check if the id is already in the database
    id_query = users.query.filter_by(id=user_id).first()
    while id_query is not None:
        user_id = str(uuid.uuid4())
        id_query = users.query.filter_by(id=user_id).first()



    user = users(id=user_id, username=user_name, email=user_email, password=user_password, pfp_id=None, remarks=None)
    db.session.add(user)
    db.session.commit()
    ret = {'access_token': guard.encode_jwt_token(user)}
    return jsonify(ret), 201


@app.route('/login', methods=['POST'])
def user_login():
    """
    Route for user login
    Args:
        email(string): Email of the user
        password(string): password of the user

    return: JWT token for authentication
    """
    
    # Retrieving request data
    user_data = request.json
    user_email = user_data.get("email")
    user_password = user_data.get("password")

    # Query database for matching email and password pair
    user = users.query.filter_by(email=user_email,password=user_password).first()

    # If user is found return JWT authentication token to frontend
    if user is not None:
        ret = {'access_token': guard.encode_jwt_token(user)}
        return jsonify(ret), 200
    
    return "Email or Password Incorrect", 401


# Under the assumption that email can not be changed
@app.route('/profile', methods=['GET', 'POST'])
@auth_required
def view_profile():
    """
    Route for getting and editing the user profile

    Header:
        Requires token in header in format:
        Authorization : Bearer <INSERT JWT TOKEN> 

     POST Args:
        password(string): Password of the user
        newpassword(string): New password of the user
        newpasswordconfirmation(string): Repeat of user's new password for confirmation
        remarks(string): Remarks on the users profile

    return: 
        GET: Returns current user email remarks and profile picture TODO yet to implement profile picture
        POST: Returns new password and remarks (FOR TESTING) TODO change to success message
    """

    # Checks if the user's token is blacklisted via logout
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    
    id = current_user_id()


    if request.method == 'GET':
        # Queries and returns profile data that should be autofilled
        user = users.query.get_or_404(id)
        return {"email":user.email, "remarks":user.remarks}, 200
    else:
        # Retrieving request data
        profile_input = request.json
        user_password = profile_input.get("password")
        new_password = profile_input.get("newpassword")
        new_password_confirmation = profile_input.get("newpasswordconfirmation")
        remarks = profile_input.get("remarks")

        user = users.query.get_or_404(id)

        # Checks if password given matches password in DB
        if user.password != user_password:
            return "Passwords do not match", 401

        # Checks if new passwords are not empty and match before changing the users password in DB
        if new_password is not None and new_password_confirmation is not None:
            if new_password != new_password_confirmation:
                return "new password does not match", 400
            user.password = new_password

        # If the remarks are not the same as the DB then edit
        if user.remarks != remarks:
            user.remarks = remarks
        db.session.commit()

        return {"new_password": user.password, "new_remark": user.remarks},200


@app.route('/logout', methods=['GET','POST'])
@auth_required
def user_logout():
    """
    Route for user logout
    return: Logout message and status code
    """

    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is already logged out", 401
    # Stores the token and its expiry date in the DB to prevent use unauthorized use of old tokens
    BlackToken = token_blacklist(token=guard.read_token_from_header(),expiry_date=datetime.fromtimestamp(guard.extract_jwt_token(guard.read_token_from_header())['exp']))
    db.session.add(BlackToken)
    db.session.commit()

    return "You have been logged out", 200


# IMAGE/VIDEO FUNCTIONS ---------------------------------------------------------------------------
@app.route('/prediction', methods=['POST']) #TODO add refrigerated conditions
@auth_required
def add_content():
    """
    Route to add a new photo/video

    Args:
        file(): Password of the user
        newpassword(string): New password of the user
        newpasswordconfirmation(string): Repeat of user's new password for confirmation
        remarks(string): Remarks on the users profile


    return: Status code
    """
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401    
    
    # Retrieve data from request
    file = request.files["file"]
    fruit_type = request.form.get("fruittype")
    location = request.form.get("location")
    
    # Checks if the file exists
    if file.filename == "":
        return "Upload a file", 400
    
    # Checks if image is in wrong format
    if not allowed_file(file.filename):
        return "Upload png or jpeg image only", 400
    
    # Generate new image id
    image_id = str(uuid.uuid4())
    # Check if the uid is already in the database
    pid_query = images.query.filter_by(pid=image_id).first()
    while pid_query is not None:
        image_id = str(uuid.uuid4())
        pid_query = images.query.filter_by(pid=image_id).first()
    
    
    # Get temperature and humidity from weather api from city 
    temperature = get_temperature(location.lower())

    humidity = get_humidity(location.lower())


    predicted_expiry = None # Create a thread to call the AI engine while the rest of the data gets sent to db

    # Add image metadata to database
    image = images(pid = image_id,
    id = current_user_id(), 
    prediction = None,
    feedback = None,
    upload_date = datetime.now(),
    purchase_date = datetime.now(),
    consume_date = datetime.now(),
    fruit = fruit_type.lower(),
    temperature = temperature,
    humidity =  humidity,
    consumed = None,
    alert_day= None,
    data = file.read())

    db.session.add(image)
    db.session.commit()

    return f"Uploaded {file.filename}",200



@app.route('/history', methods=['GET'])
@auth_required
def get_user_records():
    """
    Route to get all images/videos posted by the user
    return:
    """
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    # Get all history

    # image_query = images.query.filter_by(pid=pid).first()

    # View button (Return path to image in content folder)
    # image_path = image_query.path

    # Consume/Unconsume button
    # image_query.consumed = not image_query.consumed
    # db.session.commit()


    # Delete button
    # db.session.delete(image_query)
    # db.session.commit()


@app.route('/history', methods=['POST'])
@auth_required
def add_feedback():
    """
    Route to add feedback expiry date
    return:
    """
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    return



if __name__ == '__main__':
    app.run(port=5005)
