from flask import Flask, request

app = Flask(__name__)

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

    return

@app.route('/login', methods=['POST'])
def user_login():
    """
    Route for user login
    return: 
    """

    return

@app.route('/logout', methods=['POST'])
def user_logout():
    """
    Route for user logout
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

if __name__ == '__main__':
    app.run(port=5005)
