from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

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

@app.route('/register', methods=['POST'])
def user_register():
    """
    Route to create a new user
    return:
    """
    user_data = request.json
    user_email = user_data.get("email")
    user_password = user_data.get("password")
    user_name = user_data.get("name")
    user_id = str(uuid.uuid4())

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



    return "Email or Password Incorrect", 401

@app.route('/logout', methods=['POST'])
def user_logout():
    """
    Route for user logout
    return:
    """

    return

@app.route('/password', methods=['POST'])
def user_change_password():
    """
    Route to change passwordS
    return:
    """

    return

@app.route('/prediction', methods=['POST'])
def add_content():
    """
    Route to add a new photo/video
    return:
    """

    return

@app.route('/history', methods=['GET'])
def get_user_records():
    """
    Route to get all images/videos posted by the user
    return:
    """
    return

@app.route('/history', methods=['POST'])
def add_feedback():
    """
    Route to add feedback expiry date
    return:
    """

    return

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



if __name__ == '__main__':
    app.run(port=5005)
