from flask import Flask, jsonify, request
from user import create_user, authenticate_user, edit_profile, set_current_user
from content import process_content
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian, auth_required, current_user_id
from flask_cors import CORS
from datetime import datetime
import uuid
import shutil
import os
from weather import get_temperature, get_humidity, get_current_date

contentdb = "backend/content/" # Folder stores all the image/video files

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
    
    @property # the library needs rolenames even when disabled in the config
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

    
    

# create the database if it does not exist
app.app_context().push()
db.init_app(app)
with app.app_context():
    db.create_all()
# Initialize the flask-praetorian instance for the app
guard.init_app(app, users)
# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)

def isTokenInBlacklist(token):
    dbToken = token_blacklist.query.get(token)
    if dbToken is None:
        return False
    return True

# USER FUNCTIONS ----------------------------------------------------------------------------------
@app.route('/register', methods=['POST'])
def user_register():
    """
    Route to create a new user
    return: Success/Error message, Success/Error code
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
    return:
    """
    user_data = request.json
    user_email = user_data.get("email")
    user_password = user_data.get("password")

    user = users.query.filter_by(email=user_email,password=user_password).first()
    if user is not None:
        ret = {'access_token': guard.encode_jwt_token(user)}
        return jsonify(ret), 200
    return "Email or Password Incorrect", 401


# TODO add profile picture addtion # Assuming email is auto filled and can be changed
# TODO should return remarks and pfp as well
@app.route('/profile', methods=['GET', 'POST'])
@auth_required
def view_profile():
    """
    Route for editing user profile
    return:
    """
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    id = current_user_id()
    if request.method == 'GET':
        user = users.query.get_or_404(id)
        return {"email":user.email, "remarks":user.remarks}, 200
    else:
        profile_input = request.json
        user_password = profile_input.get("password")
        new_password = profile_input.get("newpassword")
        new_password_confirmation = profile_input.get("newpasswordconfirmation")
        remarks = profile_input.get("remarks")

        user = users.query.get_or_404(id)

        if user.password != user_password:
            return "Passwords do not match", 401

        if new_password is not None and new_password_confirmation is not None:
            if new_password != new_password_confirmation:
                return "new password does not match", 400
            user.password = new_password
        if user.remarks != remarks:
            user.remarks = remarks
        db.session.commit()

        return {"new_password": user.password, "new_remark": user.remarks},200


@app.route('/logout', methods=['GET','POST'])
@auth_required
def user_logout():
    """
    Route for user logout
    return:
    """
    BlackToken = token_blacklist(token=guard.read_token_from_header(),expiry_date=datetime.fromtimestamp(guard.extract_jwt_token(guard.read_token_from_header())['exp']))
    db.session.add(BlackToken)
    db.session.commit()

    return "You have been logged out", 200


# IMAGE/VIDEO FUNCTIONS ---------------------------------------------------------------------------
@app.route('/prediction', methods=['POST'])
@auth_required
def add_content():
    """
    Route to add a new photo/video
    return: Prediction Date
    """
    
    file = request.files["file"]
    
    fruit_type = request.form.get("fruittype")
    location = request.form.get("location")
    
    # Generate new image id
    image_id = str(uuid.uuid4())
    # Check if the uid is already in the database
    pid_query = images.query.filter_by(pid=image_id).first()
    while pid_query is not None:
        image_id = str(uuid.uuid4())
        pid_query = images.query.filter_by(pid=image_id).first()
    
    
    # Send content to AI
    temperature = None
    temperature = get_temperature(location)

    humidity = get_humidity(location)
    predicted_expiry = None # Add connection to AI here (update database when reply from AI and let the user refresh on front end)

    # Add image metadata to database

    image = images(pid = image_id,
    id = current_user_id(), 
    prediction = None,
    feedback = None,
    upload_date = datetime.now(),
    purchase_date = datetime.now(),
    consume_date = datetime.now(),
    fruit = fruit_type,
    temperature = temperature,
    humidity =  humidity,
    consumed = None,
    alert_day= None,
    data = file.read())

    db.session.add(image)
    db.session.commit()

    return f"Uploaded {file.filename}",200



@app.route('/history', methods=['GET'])

def get_user_records():
    """
    Route to get all images/videos posted by the user
    return:
    """

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
def add_feedback():
    """
    Route to add feedback expiry date
    return:
    """

    return



if __name__ == '__main__':
    app.run(port=5005)
