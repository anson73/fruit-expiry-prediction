import csv

id_filename = "backend/databases/user_id.txt" # File contains new unique user id
userdb_filename = "backend/databases/userdatabase.csv"
# Database format: [user_id, email, password, name]

current_user = None

def get_new_uid():
    """
    Get a new unique id for a user
    """
    id = int(open(id_filename, "r").read())
    idfile = open(id_filename, "w")
    idfile.write(str(id + 1))
    idfile.close()
    return id

def create_user(email, password, name):
    """
    Add a new user to the database
    return: True or False
    """

    # Check if email has already been used
    with open(userdb_filename, mode ='r') as user_db:
        db_reader = csv.reader(user_db)
        for user in db_reader:
            if user[1] == email:
                return False

    # Add user to database
    with open(userdb_filename, 'a', newline='') as user_db:
        db_writer = csv.writer(user_db)
        db_writer.writerow([get_new_uid(), email, password, name])
    
    return True

def get_user_details(user_id):
    """
    Get user details from the database
    return: [user_id, email, password, name]
    """

    with open(userdb_filename, mode ='r') as user_db:
        db_reader = csv.reader(user_db)
        for user in db_reader:
            if user[0] == str(user_id):
                return user

def authenticate_user(email, password):
    """
    Authenticate user for login
    return: True or False
    """

    with open(userdb_filename, mode ='r') as user_db:
        db_reader = csv.reader(user_db)
        for user in db_reader:
            if user[1] == email:
                if user[2] == password: 
                    set_current_user(int(user[0]))
                    return True
                else:
                    return False
    
    return False

def set_current_user(user_id):
    global current_user 
    current_user = user_id

def get_current_user():
    return current_user

if __name__ == '__main__':
    None
    # Tests: 
    # create_user("joe@gmail.com", "samplepassword123", "Joe")
    # print(get_user_details(0))
