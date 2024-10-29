from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, desc
from flask_praetorian import Praetorian, auth_required, current_user_id
from flask_cors import CORS
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import uuid
import shutil
import os
from weather import get_temperature, get_humidity, get_current_date
import atexit
from flask_apscheduler import APScheduler

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# DEFAULT_PICTURE_PATH = 'Asset/Default.png'

import base64
image_data = "data:image/png;base64,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"
directory = "Asset"
DEFAULT_PICTURE_PATH = os.path.join(directory, "Default.png")
image_data = image_data.split(",")[1]
if not os.path.exists(directory):
    os.makedirs(directory)

with open(DEFAULT_PICTURE_PATH, 'wb') as file:
    file.write(base64.b64decode(image_data))

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
app.config['SCHEDULER_API_ENABLED'] = True
# Initalise the database, JWT token libray, CORS and Scheduler
db = SQLAlchemy()
guard = Praetorian()
cors = CORS()
scheduler = APScheduler() 
# Create database model (add authentication session token)
class users(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    profile_picture = db.Column(db.LargeBinary, default = None)

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
    pid = db.Column(db.Integer, primary_key = True)
    id = db.Column("id", db.ForeignKey(users.id))
    prediction = db.Column(db.Integer)
    feedback = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    purchase_date = db.Column(db.DateTime)
    consumed = db.Column(db.Boolean, default=False)
    consume_date = db.Column(db.DateTime, default=None)
    fruit = db.Column(db.String(20))
    temperature = db.Column(db.Integer)
    humidity =  db.Column(db.Integer)
    notification_days = db.Column(db.Integer, default=0)
    disposed = db.Column(db.Boolean, default=False)
    dispose_date = db.Column(db.DateTime, default=None)
    data = db.Column(db.LargeBinary)
    notified = db.Column(db.Boolean, default = False)

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

# Checks if the token has been logged out
def isTokenInBlacklist(token):
    dbToken = token_blacklist.query.filter_by(token=token).one_or_none()
    if dbToken is None:
        return False
    return True

# Checks if the file is in correct format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# SCHEDULED FUNCTIONS ----------------------------------------------------------------------------------
@scheduler.task('interval', id='blacklist', hours = 2)
def ClearBlacklist():
    with scheduler.app.app_context():
        query = token_blacklist.query.all()
        counter = 0
        for token in query:
            if token.expiry_date < datetime.now():
                db.session.delete(token)
                db.session.commit()
                counter += 1
        print(f"{counter} Tokens cleared from the blacklist")

@scheduler.task('interval', id='Alert', hours = 6) # 6 hours
def EmailAlert():
    with scheduler.app.app_context():
        query = images.query.all()
        for image in query:
            if image.prediction:
                if image.upload_date + timedelta(days=image.prediction) < datetime.now() + timedelta(days=image.notification_days):
                    if image.notified is False:
                        image.notified = True
                        db.session.commit()
                        email = users.query.filter_by(id = image.id).first().email
                        print(f"To {email} {image.fruit} is expiring")
            
                
    



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

    with open(DEFAULT_PICTURE_PATH, 'rb' ) as file:
        blobdata = file.read()

    user = users(id=user_id, username=user_name, email=user_email, password=user_password, profile_picture=blobdata)
    db.session.add(user)
    db.session.commit()
    
    # Test
    all_users = users.query.all()
    for user in all_users:
        print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")
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
    # all_users = users.query.all()
    # for user in all_users:
    #     print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")
    print(user)
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

    return: 
        GET: Returns current user email
        POST: Returns new password(FOR TESTING)
    """

    # Checks if the user's token is blacklisted via logout
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    
    id = current_user_id()

    if request.method == 'GET':
        # Queries and returns profile data that should be autofilled
        user = users.query.get_or_404(id)
        # print(user)
        # print(user.profile_pictture)
        return {"email":user.email, "default_days": user.default_days}, 200
    else:
        # Retrieving request data
        profile_input = request.json
        user_password = profile_input.get("password")
        new_password = profile_input.get("newpassword")
        new_password_confirmation = profile_input.get("newpasswordconfirmation")
        notification_days = profile_input.get("defaultdays")

        return_string = ""
        user = users.query.get_or_404(id)

        # Checks if password given matches password in DB
        if user.password != user_password:
            return "Passwords do not match", 401

        # Checks if new passwords are not empty and match before changing the users password in DB
        if new_password is not None and new_password_confirmation is not None:
            if new_password != new_password_confirmation:
                return "new password does not match", 400
            user.password = new_password
            return_string = "Password changed"

        if user.default_days != notification_days:
            user.default_days = notification_days
            if return_string == "":
                return_string = "Default notification day changed"
            else:
                return_string += " and default notification day changed"

        db.session.commit()
        if return_string == "":
            return_string = "Nothing new"

        return return_string,200


@app.route('/logout', methods=['POST'])

def user_logout():
    """
    Route for user logout

    Header:
        Requires token in header in format:
        Authorization : Bearer <INSERT JWT TOKEN>

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
@app.route('/profile/picture/view', methods=['GET']) 
@auth_required
def get_picture():

    """
    Route to view profile picture

    Header:
        Requires token in header in format:
        Authorization : Bearer <INSERT JWT TOKEN>

    return: image
    """

    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    id = current_user_id()

    # Queries and returns profile data that should be autofilled
    user = users.query.get_or_404(id)
    return user.profile_picture


@app.route('/profile/picture', methods=['POST']) 
@auth_required
def add_picture():
    """
    Route to add a new profile picture

    Header:
        Requires token in header in format:
        Authorization : Bearer <INSERT JWT TOKEN>

    Args:
        file(file): Password of the user


    return: image
    """
    # Checks if the user's token is blacklisted via logout
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    
    id = current_user_id()

    file = request.files["file"]
    user = users.query.filter_by(id=id)
    user.profile_picture = file.read()
    db.session.commit()

    return user.profile_picture

@app.route('/prediction', methods=['POST'])
@auth_required
def add_content():
    """
    Route to add a new photo/video

    Header:
        Requires token in header in format:
        Authorization : Bearer <INSERT JWT TOKEN>

    Args:
        file(file): Password of the user
        newpassword(string): New password of the user
        newpasswordconfirmation(string): Repeat of user's new password for confirmation


    return: Status code
    """
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401    
    
    # Retrieve data from request
    file = request.files["file"]
    fruit_type = request.form.get("fruittype")
    location = request.form.get("location")
    refrigerated = bool(request.form.get("refrigerated"))
    
    # Checks if the file exists
    if file.filename == "":
        return "Upload a file", 400
    
    # Checks if image is in wrong format
    if not allowed_file(file.filename):
        return "Upload png or jpeg image only", 400
    
    # Generate new image id
    image_id = uuid.uuid4().int & (1<<32) -1
    # Check if the uid is already in the database
    pid_query = images.query.filter_by(pid=image_id).first()
    while pid_query is not None:
        image_id = uuid.uuid4().int & (1<<32) -1
        pid_query = images.query.filter_by(pid=image_id).first()
    
    
    # Get temperature and humidity from weather api from city 
    if refrigerated:
        temperature = 3
        humidity = 40
    else:
        temperature = get_temperature(location.lower())
        humidity = get_humidity(location.lower())


    predicted_expiry = None # Create a thread to call the AI engine while the rest of the data gets sent to db

    # Add image metadata to database
    image = images(pid = image_id,
    id = current_user_id(), 
    prediction = None,
    feedback = None,
    upload_date = datetime.now(),
    purchase_date = None,
    consume_date = None,
    fruit = fruit_type.lower(),
    temperature = temperature,
    humidity =  humidity,
    consumed = False,
    data = file.read())

    db.session.add(image)
    db.session.commit()

    return f"Uploaded {file.filename}",200



@app.route('/history', methods=['GET'])
def get_user_records():
    """
    Route to get all images/videos posted by the user
    return: List of Dictionaries
    """
    # Previous Example: /history?filter=unhide&page=1&size=5&sort=temperature&order=asc
    # Updated Example: /history?consumed=unhide&disposed=unhide&page=1&size=5&sort=temperature&order=asc
    query = request.args.to_dict(flat=False)

    uid = "e8a6c043-aa64-4a25-8d2b-7881d7b4e5a9" # User id hardcoded.
    if query["consumed"][0] == "hide": 
        filters = images.query.filter_by(id=uid, consumed=False)
    else:
        filters = images.query.filter_by(id=uid)

    if query["disposed"][0] == "hide": 
        filters = filters.filter_by(id=uid, disposed=False)

    count = filters.count()
    
    order_with = None
    match query["sort"][0]:
        case "imageId": order_with = "pid"
        case "fruitType": order_with = "fruit"
        case "uploadTime": order_with = "upload_date"
        case "humidity": order_with = "humidity"
        case "temperature": order_with = "temperature"
        case "purchaseDate": order_with = "purchase_date"
        case "expiryDate": order_with = "prediction"
        case "daysNotify": order_with = "notification_days"
        case "consumeDate": order_with = "consume_date"
        case "disposeDate": order_with = "dispose_date"
    
    if query["order"][0] == "desc": 
        filters = filters.order_by(desc(text(order_with)))
    else: 
        filters = filters.order_by(text(order_with))
    

    offset = (int(query["page"][0])-1)*int(query["size"][0])
    filters = filters.offset(offset).limit(int(query["size"][0]))

    result = []
    for image in filters.all():
        # Convert prediction(integer days) to a date
        if image.prediction:
            prediction = image.upload_date + timedelta(days=image.prediction)
        else: 
            prediction = None

        result.append({
            "imageId": image.pid,
            "fruitType": image.fruit,
            "uploadTime": image.upload_date,
            "humidity": image.humidity,
            "temperature": image.temperature,
            "purchaseDate": image.purchase_date,
            "expiryDate": prediction,
            "daysNotify": image.notification_days,
            "consumed": image.consumed,
            "consumedDate": image.consume_date,
            "disposed": image.disposed,
            "disposedDate": image.dispose_date
            })

    return jsonify(result, count)

@app.route('/history/unconsume', methods=['POST'])
def unconsume():
    """
    Route to change the consumed status of an image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/unconsume?imageid=1

    image_id = int(request.args.get('imageid'))
    consume_image = images.query.filter_by(pid=image_id).first()
    if not consume_image:
        return "Image id not found", 404
    
    # Check if image is already disposed
    if consume_image.disposed:
        return "Image already disposed. Cannot unconsume", 409
    
    consume_image.consume_date = None
    consume_image.consumed = not consume_image.consumed
    db.session.commit()

    return "Image consumption status changed", 200

@app.route('/history/consume', methods=['POST'])
def consume():
    """
    Route to directly change the consumed date of the image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/consume?imageid=4&days=4

    image_id = int(request.args.get('imageid'))
    consume_image = images.query.filter_by(pid=image_id).first()
    if not consume_image:
        return "Image id not found", 404

    # Check if image is already disposed
    if consume_image.disposed:
        return "Image already disposed. Cannot consume", 409
    
    # Change the consumed date to todays date minus days
    days_ago = int(request.args.get('days'))
    consume_image.consume_date = datetime.now() - timedelta(days_ago)

    consume_image.consumed = True
    db.session.commit()

    return "Image consumption date changed", 200

@app.route('/history/undispose', methods=['POST'])
def undispose():
    """
    Route to change the disposed status of an image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/undispose?imageid=1

    image_id = int(request.args.get('imageid'))
    dispose_image = images.query.filter_by(pid=image_id).first()
    if not dispose_image:
        return "Image id not found", 404

    # Check if image is already consumed
    if dispose_image.consumed:
        return "Image already consumed. Cannot undispose", 409
    
    dispose_image.dispose_date = None
    dispose_image.disposed = not dispose_image.disposed
    db.session.commit()

    return "Image disposed status changed", 200

@app.route('/history/dispose', methods=['POST'])
def dispose():
    """
    Route to directly change the disposed date of the image
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/dispose?imageid=4&days=4

    image_id = int(request.args.get('imageid'))
    dispose_image = images.query.filter_by(pid=image_id).first()
    if not dispose_image:
        return "Image id not found", 404

    # Check if image is already consumed
    if dispose_image.consumed:
        return "Image already consumed. Cannot dispose", 409
    
    # Change the consumed date to todays date minus days
    days_ago = int(request.args.get('days'))
    dispose_image.dispose_date = datetime.now() - timedelta(days_ago)

    dispose_image.disposed = True
    db.session.commit()

    return "Image disposed date changed", 200

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

@app.route('/history/alert', methods=['GET'])
def alert():
    """
    Route to get nearly expired products from database for history page popup
    return: 200 for success, 404 if imageid not found
    """

    # Example usage: /history/alert

    uid = "e8a6c043-aa64-4a25-8d2b-7881d7b4e5a9" # User id hardcoded.

    # Get all not consumed images
    non_consumed = images.query.filter_by(id=uid, consumed=False, disposed=False)

    counter = 1
    result = []
    for image in non_consumed.all():
        # Convert prediction(integer days) to a date
        prediction = image.upload_date + timedelta(days=image.prediction)

        # If [today's date] is within [[expiry date] minus [notification days]] and [expiry date]
        if (prediction - timedelta(days=image.notification_days)) <= datetime.now() <= prediction:
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
                })

        counter += 1

    return result


@app.route('/image', methods=['GET'])
def get_image():
    image = images.query.filter_by(pid=1219339313).first()
    return image.data

@app.route('/history', methods=['POST'])
@auth_required
def add_feedback():
    """
    Route to add feedback expiry date

    Header:
        Requires token in header in format:
        Authorization : Bearer <INSERT JWT TOKEN>

    return:
    """
    if isTokenInBlacklist(guard.read_token_from_header()):
        return "This user is logged out", 401
    
    return


atexit.register(lambda: scheduler.shutdown(wait=False))
if __name__ == '__main__':
    app.run(port=5005)
