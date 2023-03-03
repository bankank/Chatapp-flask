from flask import *
from flask_login import *
from flask_socketio import *
from userauth import *
from database import *
from pymongo.errors import *
import datetime 
import requests
import os 

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")  # ,logger=True, engineio_logger=True
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"


@app.route("/")
@app.route("/home")
def home_page():

    return render_template("./home_page.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("chat_page" , group_id="me"))
    error_message = ""
    if request.method == "POST":
        save_username_registered = request.form.get("username_registered")
        save_password_registered = request.form.get("password_registered")
        date_time = datetime.datetime.now()
        user_id = date_time.strftime("%G%m%d%H%M%S%f%z")
        account_created = date_time.strftime("%d %B %A %G %H:%M:%S %p %Z | %c ")
        ip_geo = "Null"
        length_username = len(save_username_registered)
        length_password = len(save_password_registered)
        if length_username < 4 and  length_password < 8 :
            error_message = "username should be minimum 4 charater and password should be minium 8 character long"
            try:
                register_new_user_to_database(save_username_registered , save_password_registered , user_id , account_created , ip_geo)
                return redirect(url_for("login_page"))
            except DuplicateKeyError:
                error_message = "A user with that username already exists"
    return render_template("./register_page.html", error_message=error_message )



@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("chat_page" , group_id='me'))
    error_message = ""
    if request.method == "POST":
        login_username = request.form.get("login_username")
        login_password = request.form.get("login_password")
        search_foruser = login_searchuser(login_username)
        if search_foruser and search_foruser.checkpassword(login_password):
            login_user(search_foruser)
            # login_event_fetch(search_foruser)
            # return redirect(url_for('chat_page' , group_id="me" , type=None))
            return redirect(url_for('chat_page', group_id='me' , type=None))
        else:
            error_message = "You have entered an invalid username or password"
    # ff = make_response(render_template("login.html" , error_message = error_message))
    # ff.set_cookie('userID', value='jo')
    # return ff
    return render_template("login_page.html", error_message=error_message)


@app.route("/chat/<group_id>" ,methods=["GET", "POST"])
@app.route("/chat/<group_id>/<type>" ,methods=["GET", "POST"])
def chat_page(group_id,type=None):  #def chat_page(group_id,type="None"):
    
    if request.method == "POST":
        date_time = datetime.datetime.now()
        groupid = date_time.strftime("%G%m%d%H%M%S%f%z")
        group_created = date_time.strftime("%d %B %A %G %H:%M:%S %p %Z | %c ")
        group_name = request.form.get("group_name")
        usernames = [username.strip() for username in request.form.get('users').split(',')] 
        group_created_by = current_user.username
        create_group(group_name , group_created_by , groupid , group_created)
        

    if current_user.is_authenticated:
            if group_id == "me" and type==None : #    if group_id == "me" and type=="None" :
                username_profile = current_user.username
                return render_template("chat_default.html" , username_profile=username_profile)
          
            elif group_id == "create" and type == "group":
              if current_user.is_authenticated:
                nickname_displaypage = current_user.username
                # if request.method == "POST":
                    # group_name = request.form.get("group_name")
                    # print(group_name)
               
                    
                return render_template("create_group_page.html" )
            
            else :
                nickname_displaypage = current_user.username
                display_chat = get_message() 
                display_user = display_members_page()
                return render_template("chat.html", nickname_displaypage=nickname_displaypage , display_chat = display_chat, display_user = display_user)
    else:
        return redirect(url_for("home_page"))



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('page_notfound.html'), 404

@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    # kills the session other wise user can just /chat to talk again
    return redirect(url_for("home_page"))


@socketio.on("connect")
def connect_handler():
    if current_user.is_authenticated:
        print(f"{current_user.username} has joined the chat")
        date_time = datetime.datetime.now()
        date_time_user = date_time.strftime("%a %b %d %G %I:%M %p")
        emit(
            "user-connected-message",
            {"message": f"{current_user.username} has joined the chat" , "joinedat": f"{date_time_user}"},
            broadcast=True,
        )
    else:
        pass
    
@socketio.on("disconnect")
def connect_handler():
    if current_user.is_authenticated:
        print(f"{current_user.username} has left the chat")
        date_time = datetime.datetime.now()
        date_time_user = date_time.strftime("%a %b %d %G %I:%M %p")
        emit(
            "user-connected-message",
            {"message": f"{current_user.username} has left the chat" , "joinedat": f"{date_time_user}"},
            broadcast=True,
        )
    else:
        pass


@socketio.on("message")
def handle_message(message):
    if current_user.is_authenticated:
        date_time = datetime.datetime.now()
        date_time_message = date_time.strftime("%a %b %d %G %I:%M %p")
        message_id = date_time.strftime("%G%m%d%H%M%S%f%z")
        print(f"{message} and user is {current_user.username}")
        message_value = message
        message_author = current_user.username
        save_msg(message_value, message_author , date_time_message , message_id)
        emit(
            "message-user-sent",
            {"messagevalue": f"{message}", "messageuser": f"{current_user.username}" , "date_time_message":   f"{date_time_message}"},
            broadcast=True,
        )
    else:
        pass


@login_manager.user_loader
def load_user(login_username):
    return login_searchuser(login_username)


if __name__ == "__main__":
    # socketio.run(app, port=8000)
    socketio.run(app, host="localhost")
