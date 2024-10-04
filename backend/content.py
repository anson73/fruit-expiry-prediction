import csv
from weather import get_temperature

id_filename = "backend/databases/content_id.txt" # File contains new unique content id
contentdb_filename = "backend/databases/contentdatabase.csv"
# Database format: ["content_id", "content_path", "user_id", 
# "temperature", "predicted_expiry", "actual_expiry"]

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

def process_content(content, user_id, city):
    """
    Store content in the database
    return: Predicted expiry date
    """
    # Save image/video to content folder

    # Send content to AI
    temperature = get_temperature(city)
    predicted_expiry = None

    # Add content information to database
    with open(contentdb_filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([get_new_cid(), "insert_content_path_here", user_id, 
                            temperature, predicted_expiry, None])
    
    return predicted_expiry

def get_user_content(user_id):
    """
    Store content in the database
    return: ["content_id", "content_path", "user_id", 
            "temperature", "predicted_expiry", "actual_expiry"]
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
