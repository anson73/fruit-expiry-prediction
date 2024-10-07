from flask import Flask, jsonify, request
from user import create_user, authenticate_user, edit_profile, set_current_user
from content import process_content

app = Flask(__name__)

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

    # 3 scenarios: Email already used OR passwords dont match OR Account successfully created. 
    result = create_user(user_email, user_name, user_password, user_password_confirmation)

    return result[0], result[1]

@app.route('/login', methods=['POST'])
def user_login():
    """
    Route for user login
    return: 
    """

    login_input = request.json
    user_email = login_input.get("email")
    user_password = login_input.get("password")

    if not authenticate_user(user_email, user_password):
        return "Login unsuccessful", 401

    return "Login successful", 200

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
    alert_day = profile_input.get("day")

    
    if not edit_profile(user_email, user_password, new_password, new_password_confirmation, alert_day):
        return 401

    return 200

@app.route('/logout', methods=['POST'])
def user_logout():
    """
    Route for user logout
    return: 
    """

    set_current_user(None)
    return 200

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

if __name__ == '__main__':
    app.run(port=5005)
