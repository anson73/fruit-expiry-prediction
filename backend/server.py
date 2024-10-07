from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

current_user = None # Holds the id of the user that is currently logged in. 

app = Flask(__name__)
# Add databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initalise the database
db = SQLAlchemy(app)


# Create database model
class users(db.Model):
    uid = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    reminder_days = db.Column(db.Integer)
    pfp_id = db.Column(db.Integer)
    remarks = db.Column(db.String(200))

    def __repr__(self):
        return '<UID %r>' % self.uid

class images(db.Model):
    pid = db.Column(db.Integer, primary_key = True)
    prediction = db.Column(db.Integer)
    feedback = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    fruit = db.Column(db.String(20))
    temperature = db.Column(db.Integer)
    humidity =  db.Column(db.Integer)
    def __repr__(self):
        return '<PID %r>' % self.pid

class user_image(db.Model):
    uid = db.Column("uid", db.ForeignKey(users.uid))
    pid = db.Column("pid", db.ForeignKey(images.pid) ,primary_key = True)

    def __repr__(self):
        return '<PID %r>' % self.pid

with app.app_context():
    db.create_all()

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
    
    # Check if the uid is already in the database
    uid_query = users.query.filter_by(uid=user_id).first()
    while uid_query is not None:
        user_id = str(uuid.uuid4())
        uid_query = users.query.filter_by(uid=user_id).first()


    user = users(uid=user_id, username=user_name, email=user_email, password=user_password, reminder_days=None, pfp_id=None, remarks=None)
    set_current_user(user.uid)
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

    if login_query is not None:
        return str(login_query), 200

    set_current_user(login_query.uid)
    return "Email or Password Incorrect", 401


@app.route('/profile', methods=['POST'])
def edit_profile():
    """
    Route for editing user profile
    return: 
    """

    profile_input = request.json
    user_email = profile_input.get("email")
    user_password = profile_input.get("password")
    new_password = profile_input.get("newpassword")
    new_password_confirmation = profile_input.get("newpasswordconfirmation")
    reminder_days = profile_input.get("day")
    remarks = profile_input.get("remarks")

    # Check if passwords match
    if new_password != new_password_confirmation:
        return "Passwords do not match", 400
    
    # Authenticate User
    user_profile = users.query.filter_by(email=user_email,password=user_password).first()
    if user_profile is None:
        return "Email or Password Incorrect", 401

    # Update user profile
    user_profile.password = new_password
    user_profile.password = reminder_days
    user_profile.remarks = remarks
    db.session.commit()
    return 200


@app.route('/logout', methods=['POST'])
def user_logout():
    """
    Route for user logout
    return:
    """

    set_current_user(None)
    return 200

@app.route('/password', methods=['POST'])
def user_change_password():
    """
    Route to change passwordS
    return:
    """

    set_current_user(None)
    return 200

@app.route('/profile', methods=['GET'])
def get_profile_picture():
    """
    Route to get profile picture
    return: Profile Picture
    """

    return

@app.route('/profile', methods=['POST'])
def add_profile_picture():
    """
    Route to add/change profile picture
    return:
    """

    return

# IMAGE/VIDEO FUNCTIONS ---------------------------------------------------------------------------
@app.route('/prediction', methods=['POST'])
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

    expiry_date = process_content(file, fruit_type, location, refrigeration, purchase_date)
    return jsonify({"prediction":expiry_date})

@app.route('/history', methods=['GET'])
def get_user_records():
    """
    Route to get all images/videos posted by the user
    return:
    """

    # View: content -> get_image
    # Consume/Unconsume: content -> consume
    # Delete: content -> delete_content

    return

@app.route('/history', methods=['POST'])
def add_feedback():
    """
    Route to add feedback expiry date
    return:
    """

    return

def set_current_user(user_id):
    global current_user
    current_user = user_id


if __name__ == '__main__':
    app.run(port=5005)
