import csv
import shutil
from weather import get_temperature
from user import get_current_user

contentdb = "backend/content" # Folder stores all the image/video files
id_filename = "backend/databases/content_id.txt" # File contains new unique content id
contentdb_filename = "backend/databases/contentdatabase.csv"
# Database format: ["content_id", "content_path", "user_id", "fruit_type", 
# "temperature", "predicted_expiry", "actual_expiry", "purchase_date"]

def get_new_cid():
    """
    Get a new unique id for an image/video
    return: integer id
    """
    id = int(open(id_filename, "r").read())
    idfile = open(id_filename, "w")
    idfile.write(str(id + 1))
    idfile.close()
    return id

def process_content(file, fruit_type, location, refrigeration, purchase_date):
    """
    Store content in the database
    return: Predicted expiry date
    """
    # Save image/video to content folder
    content_id = get_new_cid()
    
    content_path = None #

    # Send content to AI
    temperature = None
    if refrigeration: 
        temperature = refrigeration
    else: 
        temperature = get_temperature(location)

    predicted_expiry = None # Add connection to AI here

    # Add content information to database
    with open(contentdb_filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([content_id, content_path, get_current_user, fruit_type, 
                         temperature, predicted_expiry, None, purchase_date])
    
    return predicted_expiry

def get_user_content(user_id):
    """
    Store content in the database
    return: []
    """

    with open(contentdb_filename, mode ='r') as content_db:
        db_reader = csv.reader(content_db)
        for content in db_reader:
            if content[2] == str(user_id):
                return content


if __name__ == '__main__':
    None
    # Tests:
    # process_content(None, 0, "sydney")
    # print(get_user_content(0))
