from pymongo import MongoClient
from userauth import User
from bson import ObjectId
import datetime 
client = MongoClient(
    "mongodb+srv://readdata:readdata@chatappmongo.7t9qbkj.mongodb.net/?retryWrites=true&w=majority"
)


chat_app_flask = client.get_database("chat_app_flask")
userdata = chat_app_flask.get_collection("userinfo")
login_event = chat_app_flask.get_collection("login_events")
msgs =  chat_app_flask.get_collection("Message")
display_members = chat_app_flask.get_collection("displaymembers")



def register_new_user_to_database(save_username_registered , save_password_registered , user_id , account_created , ip_geo): 
    userdata.insert_one(
        {"_id": save_username_registered,"Username": save_username_registered, "Password": save_password_registered , "User_id":user_id ,"Account_created":account_created , "IP-GEO":ip_geo} 
    )


def login_searchuser(search_foruser):
    find_user = userdata.find_one({"_id": search_foruser})
    return User(find_user["_id"], find_user["Password"]) if find_user else None


def save_msg(message_value , message_author , date_time_message , message_id):
    msgs.insert_one({"message":message_value , "message_author": message_author , "date_time_message": date_time_message , "message_id": message_id} )
    
def login_event(user_id , username , timestamp , ip_geo):
    login_event.insert_one({"user_id":user_id,"Username":username , "Timestamp":timestamp,"IP-GEO":ip_geo})
    
# def login_event_fetchdata(search_foruser):
#     login_event_fetch = userdata.find_one({"_id": search_foruser})
#     return ("f") if login_event_fetch  else None

# def login_event_fetch(search_foruser):
#     fetch_data = userdata.find_one({"_id": search_foruser})
#     return User(fetch_data["Password"] , fetch_data["User_id"])
    
    
    
def get_message():
    return list(msgs.find())

def display_members_page():
    return list(display_members.find())


groups_list = chat_app_flask.get_collection("Groups")
groups_user = chat_app_flask.get_collection("Groups_users")

def create_group(group_name , group_created_by , groupid , group_created):
    groups_list.insert_one({"Group_Id": groupid , "Group_name":group_name , "group_created_by" :group_created_by , "group_created":group_created})



