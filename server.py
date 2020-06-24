from flask import Flask, request 
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_restful import reqparse
from sqlite3 import connect #default library in python
#every other package isn't default, run python setup.py

app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

#convert tuples to dictionaries
def _convert_to_beautiful_post(raw_post):
    return {"recipient": raw_post[0], "content": raw_post[1]}

class PostList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("recipient", type=str, help="For who you send this message you")
        self.parser.add_argument("content", type=str, help="Content of your message")

    def get(self):
        raw_posts = fetch_messages() #WOY SASKIA

        # Parse and return the result
        return {"posts": [_convert_to_beautiful_post(raw_post) for raw_post in raw_posts]}

    def post(self):
        # Parse the input data
        args = self.parser.parse_args()
        recipient = args["recipient"]
        content = args["content"]

        insert_new_message(recipient, content) #WOY SAS

        # Parse and return the result
        return _convert_to_beautiful_post([recipient, content])

api.add_resource(PostList, "/posts") #connects to the URL /posts
#What is PostList?

#===== Don't edit anything above this line ==================================

#replace vowels in content with recipient and vowels in recipient with content
def replace_vowels(recipient, content):
    vowels = ["a" , "A", "E" ,"e" ,"I" ,"i","O", "o","U", "u"]
    i = len(vowels) - 1
    
    while i >= 0 : # eq bc i eq to 0 after index = 1 (line 50)
        content = content.replace(vowels[i], recipient) #must be assigned to a variable
        i -= 1
    
    return(content)


def fetch_messages():
    connection = connect("transformed_texts.db")#must be stored in some variable
    query = "SELECT recipients, messages FROM secret_messages ORDER BY rowid DESC"
    
    query_result = connection.execute(query).fetchall()
    
    return query_result 


#insert the recipient and content to the database
def insert_new_message(recipient, content):
    connection = connect("transformed_texts.db")
    
    if len(recipient) > 0 and len(content) > 0:
        content = replace_vowels(recipient, content)
        query = "INSERT INTO secret_messages (recipients, messages) VALUES ('{}' , '{}')".format(recipient, content)
        connection.execute(query)
        connection.commit()


#===== Don't edit anything below this line ==================================
if __name__ == "__main__":
     app.run(port="8000")
