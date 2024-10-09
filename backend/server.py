from flask import Flask, jsonify, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from user import create_user, authenticate_user, edit_profile, set_current_user
from content import process_content
from flask_sqlalchemy import SQLAlchemy
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
# add secret key
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
# Initalise the database
db = SQLAlchemy()


# Create database model (add authentication session token)
class users(db.Model, UserMixin):
    id = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    alert_day = db.Column(db.Integer)
    pfp_id = db.Column(db.Integer)
    remarks = db.Column(db.String(200))

    def __repr__(self):
        return '<UID %r>' % self.id

class images(db.Model):
    pid = db.Column(db.Integer, primary_key = True)
    id = db.Column("id", db.ForeignKey(users.id))
    prediction = db.Column(db.Integer)
    feedback = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    purchase_date = db.Column(db.DateTime)
    consume_date = db.Column(db.DateTime)
    fruit = db.Column(db.String(20))
    temperature = db.Column(db.Integer)
    humidity =  db.Column(db.Integer)
    path = db.Column(db.String(100))
    consumed = db.Column(db.Boolean)

    def __repr__(self):
        return '<PID %r>' % self.pid

# create the database if it does not exist
app.app_context().push()
db.init_app(app)
with app.app_context():
    db.create_all()

# create an instance of the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Assign Login View
login_manager = LoginManager()
# Redirect to the login page if authentication fails
login_manager.login_view = "login" #TODO REDIRECT LOGIN PAGE
login_manager.init_app(app)


# Query user from the database based on id
@login_manager.user_loader
def load_user(id):
    # Query user from database based on id
    return users.query.get(id)

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



    user = users(id=user_id, username=user_name, email=user_email, password=user_password, alert_day=None, pfp_id=None, remarks=None)
    db.session.add(user)
    db.session.commit()
    return "Account Sucessfully Created", 201


@app.route('/login', methods=['POST'])
def user_login():
    """
    Route for user login
    return:
    """
    user_data = request.json
    user_email = user_data.get("email")
    user_password = user_data.get("password")

    login_query = users.query.filter_by(email=user_email,password=user_password).first()

    login_user(login_query, remember=True)

    if login_query is not None:
        return str(login_query), 200
      
    return "Email or Password Incorrect", 401


# TODO add profile picture addtion # Assuming email is auto filled and can be changed
# TODO should return remarks and pfp as well
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    """
    Route for editing user profile
    return:
    """
    id = current_user.id
    if request.method == 'GET':
        user = users.query.get_or_404(id)
        return {"email":user.email, "remarks":user.remarks, "alert_day": user.alert_day}, 200
    else:
        profile_input = request.json
        user_password = profile_input.get("password")
        new_password = profile_input.get("newpassword")
        new_password_confirmation = profile_input.get("newpasswordconfirmation")
        alert_day = profile_input.get("day")
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
        user.alert_day = alert_day
        db.session.commit()

        return {"new_password": user.password, "new_remark": user.remarks, "alert_day": user.alert_day},200


@app.route('/logout', methods=['GET','POST'])
@login_required
def user_logout():
    """
    Route for user logout
    return:
    """
    logout_user()
    return "you have been logged out", 200


# IMAGE/VIDEO FUNCTIONS ---------------------------------------------------------------------------
@app.route('/prediction', methods=['POST'])
@login_required
def add_content():
    """
    Route to add a new photo/video
    return: Prediction Date
    """

    content_data = request.json
    file = content_data.get("file")
    fruit_type = content_data.get("fruittype")
    location = content_data.get("location")
    refrigeration = content_data.get("refrigeration")
    purchase_date = content_data.get("purchasedate")

    # Generate new image id
    image_id = str(uuid.uuid4())
    # Check if the uid is already in the database
    pid_query = images.query.filter_by(pid=image_id).first()
    while pid_query is not None:
        image_id = str(uuid.uuid4())
        pid_query = images.query.filter_by(pid=image_id).first()

    # Save image/video to content folder
    file_name, file_type = os.path.splitext(file)
    content_path = contentdb + str(image_id) + file_type
    shutil.copy(file, content_path)

    # Send content to AI
    temperature = None
    if refrigeration: temperature = refrigeration
    else: temperature = get_temperature(location)

    humidity = get_humidity(location)
    predicted_expiry = None # Add connection to AI here (update database when reply from AI and let the user refresh on front end)

    # Add image metadata to database
    image = images(pid=image_id, prediction=predicted_expiry, feedback=None, 
                   upload_date=get_current_date(location), fruit=fruit_type, 
                   temperature=temperature, humidity=humidity, path=content_path, 
                   consumed=False, id=current_user.id)
    db.session.add(image)
    db.session.commit()

    return jsonify({"prediction":predicted_expiry})

@app.route('/history', methods=['GET'])
@login_required
def get_user_records():
    """
    Route to get all images/videos posted by the user
    return:
    """

    # Get all history
    history_query = users.query.filter_by(id=current_user)

    # image_query = images.query.filter_by(pid=pid).first()

    # View button (Return path to image in content folder)
    # image_path = image_query.path

    # Consume/Unconsume button
    # image_query.consumed = not image_query.consumed
    # db.session.commit()


    # Delete button
    # db.session.delete(image_query)
    # db.session.commit()

    return

@app.route('/history', methods=['POST'])
def add_feedback():
    """
    Route to add feedback expiry date
    return:
    """

    return



if __name__ == '__main__':
    app.run(port=5005)
