from flask import Flask, jsonify, request
from user import create_user, authenticate_user, edit_profile, set_current_user
from content import process_content
from sqlalchemy import text, desc
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian, auth_required, current_user_id
from flask_cors import CORS
from datetime import datetime, timedelta
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
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
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
    alert_day = db.Column(db.Integer)
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
    notification_days = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<PID %r>' % self.pid

# create the database if it does not exist
app.app_context().push()
db.init_app(app)
with app.app_context():
    db.create_all()
# Initialize the flask-praetorian instance for the app
guard.init_app(app, users)
# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)

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
    id = current_user_id()
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

def user_logout():
    """
    Route for user logout
    return:
    """
    return "you have been logged out", 200


# IMAGE/VIDEO FUNCTIONS ---------------------------------------------------------------------------
@app.route('/prediction', methods=['POST'])
def add_content():
    # Test: Add entry to image database. 
    
    image = images(pid=0, id=0, prediction=5, feedback=3,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = None, fruit="Apple", 
                   temperature="24", humidity="40", path="backend/content", notification_days = 1, consumed=False)
    db.session.add(image)
    db.session.commit()

    image = images(pid=1, id=0, prediction=3, feedback=4,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = None, fruit="Orange", 
                   temperature="40", humidity="10", path="backend/content", notification_days = 3, consumed=False)
    db.session.add(image)
    db.session.commit()

    image = images(pid=2, id=0, prediction=6, feedback=9,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = datetime.now(), fruit="Grape", 
                   temperature="15", humidity="33", path="backend/content", notification_days = 8, consumed=True)
    db.session.add(image)
    db.session.commit()

    # This test has a user id of 1, so it should not show in the history page
    image = images(pid=3, id=1, prediction=6, feedback=9,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = datetime.now(), fruit="Grape", 
                   temperature="15", humidity="33", path="backend/content", notification_days = 4, consumed=True)
    db.session.add(image)
    db.session.commit()

    image = images(pid=4, id=0, prediction=8, feedback=22,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = datetime.now(), fruit="Apple", 
                   temperature="3", humidity="40", path="backend/content", notification_days = 2, consumed=True)
    db.session.add(image)
    db.session.commit()

    image = images(pid=5, id=0, prediction=1, feedback=2,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = None, fruit="Bananna", 
                   temperature="6", humidity="30", path="backend/content", notification_days = 10, consumed=False)
    db.session.add(image)
    db.session.commit()

    image = images(pid=6, id=0, prediction=6, feedback=6,
                   upload_date=datetime.now(), purchase_date = datetime.now(), consume_date = None, fruit="Mango", 
                   temperature="6", humidity="30", path="backend/content", consumed=False)
    db.session.add(image)
    db.session.commit()

    """
    Route to add a new photo/video
    return: Prediction Date
    """
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
    
#----------------------------------------------------------------------------
    image = images(pid = 12,id = current_user.id, prediction = None, feedback = None,
    upload_date = datetime.now(), purchase_date = None,
    consume_date = None,
    fruit = None,
    temperature = None,
    humidity =  None,
    path = None,
    consumed = None)
    db.session.add(image)
    db.session.commit()
"""
    return "created", 200


@app.route('/history', methods=['GET'])
def get_user_records():
    """
    Route to get all images/videos posted by the user
    return: List of Dictionaries
    """
    # Example: /history?filter=unhide&page=1&size=5&sort=temperature&order=asc
    query = request.args.to_dict(flat=False)

    uid = 0 # User id hardcoded.
    if query["filter"][0] == "hide": 
        filters = images.query.filter_by(id=uid, consumed=False)
    else:
        filters = images.query.filter_by(id=uid)

    
    order_with = None
    match query["sort"][0]:
        case "imageid": order_with = "pid"
        case "fruitType": order_with = "fruit"
        case "uploadTime": order_with = "upload_date"
        case "humidity": order_with = "humidity"
        case "temperature": order_with = "temperature"
        case "purchaseDate": order_with = "purchase_date"
        case "expiryDate": order_with = "prediction"
        case "daysNotify": order_with = "notification_days"
        case "consumeDate": order_with = "consume_date"
    
    if query["order"][0] == "desc": 
        filters = filters.order_by(desc(text(order_with)))
    else: 
        filters = filters.order_by(text(order_with))
    

    offset = (int(query["page"][0])-1)*int(query["size"][0])
    filters = filters.offset(offset).limit(int(query["size"][0]))
    

    counter = 1
    result = []
    for image in filters.all():
        # Convert prediction(integer days) to a date
        prediction = image.upload_date + timedelta(days=image.prediction)

        result.append({
            "seq": counter,
            "imageId": image.pid,
            "fruitType": image.fruit,
            "uploadTime": image.upload_date,
            "humidity": image.humidity,
            "temperature": image.temperature,
            "purchaseDate": image.purchase_date,
            "expiryDate": prediction,
            "daysNotify": image.notification_days,
            "consumed": image.consumed,
            "consumedDate": image.consume_date
            })

        counter += 1

    return result

@app.route('/history/consume', methods=['POST'])
def consume():
    """
    Route to change the consumed status of an image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/consume?imageid=1

    image_id = int(request.args.get('imageid'))
    consume_image = images.query.filter_by(pid=image_id).first()
    if not consume_image:
        return "Image id not found", 404
    
    consume_image.consumed = not consume_image.consumed
    db.session.commit()

    return "Image consumption status changed", 200

@app.route('/history/notification', methods=['POST'])
def notification_days():
    """
    Route to change expiry notification days for an image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/notification?imageid=1&days=1

    image_id = int(request.args.get('imageid'))
    selected_image = images.query.filter_by(pid=image_id).first()
    if not selected_image:
        return "Image id not found", 404

    selected_image.notification_days = int(request.args.get('days'))
    db.session.commit()

    return "Notification days changed", 200

@app.route('/history/delete', methods=['DELETE'])
def delete():
    """
    Route to delete a selected image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/delete?imageid=1

    image_id = int(request.args.get('imageid'))
    delete_image = images.query.filter_by(pid=image_id).first()
    if not delete_image:
        return "Image id not found", 404

    db.session.delete(delete_image)
    db.session.commit()

    return "Image Deleted", 200

@app.route('/history', methods=['POST'])
def add_feedback():
    """
    Route to add feedback expiry date
    return:
    """

    return



if __name__ == '__main__':
    app.run(port=5005)
