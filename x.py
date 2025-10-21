"""
    x.py
    ------
    Purpose:
    - Connect to the MySQL database (db function)
    - Validate user input (names, email, password)
    - Provide a no_cache decorator to prevent showing cached pages after logout

    Notes:
    - Only some validators are used right now (name, email, password).
    - Others (confirm password, UUID) are examples for later use.

    from flask import request, make_response, render_template
    - Import Flask utilities: request to read inputs, make_response to build HTTP responses

    import mysql.connector
    - MySQL driver used to connect to the database

    import re
    - Python's regular expressions library, used for validating input (like email/password formats)
    
    from functools import wraps
    - Used to implement decorators while preserving function metadata

    from icecream import ic
    - Import the icecream debug print tool
    
    ic.configureOutput(prefix=f'----- | ', includeContext=True)
    - Configure icecream: adds a prefix and shows context (file + line number)

    UPLOAD_ITEM_FOLDER = './images'
    - Path to the folder where uploaded files (like images) will be stored
"""
from flask import request, make_response, render_template 
import mysql.connector 
import re
from functools import wraps

import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from icecream import ic 
ic.configureOutput(prefix=f'----- | ', includeContext=True)

UPLOAD_ITEM_FOLDER = './images'


######## DATABASE CONNECTION ########
"""
    Create a connection to the database.
    - mysql.connector.connect(...) opens the connection
    - host: where the database server is running (here "mariadb" = Docker service name)
    - user: MySQL username
    - password: MySQL password
    - database: Name of the database/schema to use (here "twitter")

    cursor(dictionary=True) means:
    - Results will come back as Python dictionaries, not just tuples.
    - Example: row["user_name"] instead of row[0]
    - Create a cursor that returns results as dictionaries instead of tuples

    Returns:
    - db     -> the connection (so we can commit/rollback/close)
    - cursor -> the cursor to run SQL queries

    except Exception as e:
    - Catch any connection or driver exceptions

    - If connection fails:
    - Print the error to the terminal -> print(e, flush=True)
    - Raise a new Exception with a custom message that app.py can catch -> raise Exception("Twitter exception - Database under maintenance", 500)
"""
def db():
    try:
        host = "esterpiazza.mysql.eu.pythonanywhere-services.com" if "PYTHONANYWHERE_DOMAIN" in os.environ else "mariadb"
        user = "esterpiazza" if "PYTHONANYWHERE_DOMAIN" in os.environ else "root"
        password = "MyPasswordForYou" if "PYTHONANYWHERE_DOMAIN" in os.environ else "password"
        database = "esterpiazza$default" if "PYTHONANYWHERE_DOMAIN" in os.environ else "twitter"
        db = mysql.connector.connect(
            #host = "mariadb", 
            host = host,
            user = user,  
            password = password,
            database = database
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Twitter exception - Database under maintenance", 500)


######## NO CACHE DECORATOR ########
"""
    Decorator that disables browser caching.
    - Decorator factory: receives a view function
    - Prevents showing protected pages with Back button after logout.
    - Adds HTTP headers to force reload from server.
    
    def no_cache_view(*args, **kwargs):
    - Wrapper function that injects headers into the response
    
    response = make_response(view(*args, **kwargs))
    - Call the original view and wrap its return value as a Response

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0" 
    - Disable caching aggressively

    response.headers["Pragma"] = "no-cache" 
    - Legacy header for older HTTP/1.0 caches
    
    response.headers["Expires"] = "0" 
    - Expire the content immediately
    
    return response 
    - Return the modified response to the client

    return no_cache_view 
    - Return the wrapper so it can replace the original view

    Purpose:
    - After logout, the user should NOT be able to press the back button

    Usage:
    - @x.no_cache
    - def view_home(): ...
"""
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view


######## VALIDATION: EMAIL ########
"""
    Validate user_email from the form.
    - Get the value from request.form (default empty string if missing)
    - Remove spaces
    - If the email does not match the REGEX_EMAIL
    - If invalid, raise an Exception (so app.py can return "Invalid email")
"""
REGEX_EMAIL = r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
def validate_user_email():
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_EMAIL, user_email): raise Exception("Invalid email", 400)
    return user_email

######## VALIDATION: USERNAME / FIRST NAME ########
"""
    USER_NAME_MIN = 2
    - Minimum allowed length for user_name
    
    USER_NAME_MAX = 20 
    - Maximum allowed length for user_name

    def validate_user_name(user_name: str):
    - Validate the username length and trim whitespace

    if len(user_name) < USER_NAME_MIN: 
    - If shorter than minimum, reject
    
    raise Exception("Twitter exeption - user name too short") 
    - Raise a descriptive error message
    
    if len(user_name) > USER_NAME_MAX:
    - If longer than maximum, reject
    
    return user_name.strip()
    - Return the cleaned value (leading/trailing spaces removed)

"""
# ---------- USER NAME ----------
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
#REGEX_USER_USERNAME = f"^.{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
# TODO: The username can only be english letters 2 to 20 and contain 1 underscore
REGEX_USER_USERNAME = f"^(?!.*_.*_)[A-Za-z_]{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
# REGEX_USER_USERNAME = f"^.{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$" # changed the regex to a . 


def validate_user_username():
    user_username = request.form.get("user_username", "").strip()
    user_username = user_username.lower() # making the username lowercase
    error = f"username min {USER_USERNAME_MIN} max {USER_USERNAME_MAX} characters" # a variable
    if not re.match(REGEX_USER_USERNAME, user_username): raise Exception(error, 400) # if something goes wrong. re.match is imported. 
    # if len(user_username) < USER_USERNAME_MIN: raise Exception(error, 400)
    # if len(user_username) > USER_USERNAME_MAX: raise Exception(error, 400)
    return user_username


######## VALIDATION: PASSWORD ########
"""
    Validate password from the form.
    - Must be 4–50 characters (for easy testing now, can be increased later)
    
    def validate_user_password():
    - Validate the password from the form
    
    user_password = request.form.get("user_password", "").strip()
    - Read password input and trim whitespace
    
    if not re.match(REGEX_USER_PASSWORD, user_password):
    - Uses regex to check the length

    raise Eception:
    - If invalid, raise Exception
"""
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password): raise Exception("Invalid password", 400)
    return user_password


# ---------- FIRST NAME ----------
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
REGEX_FIRST_NAME = f"^.{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$"
def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    error = f"first name min {USER_FIRST_NAME_MIN} max {USER_FIRST_NAME_MAX} characters"
    if len(user_first_name) < USER_FIRST_NAME_MIN: raise Exception(error, 400)
    if len(user_first_name) > USER_FIRST_NAME_MAX: raise Exception(error, 400)
    return user_first_name

# ---------- LAST NAME ----------
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
REGEX_LAST_NAME = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    error = f"last name min {USER_LAST_NAME_MIN} max {USER_LAST_NAME_MAX} characters"
    if len(user_last_name) < USER_LAST_NAME_MIN: raise Exception(error, 400)
    if len(user_last_name) > USER_LAST_NAME_MAX: raise Exception(error, 400)
    return user_last_name







######## VALIDATION: PASSWORD CONFIRM ########
"""
    If the form asks the user to type the password twice,
    this function validates the second field (confirm). I don't have it thooo
    
    def validate_user_password_confirm():
    - validate the "confirm password" field (if present)
    
    user_password = request.form.get("user_password_confirm", "").strip()
    - Read confirm field and trim whitespace

    if not re.match(REGEX_USER_PASSWORD, user_password):
    - Reuse the same password regex
    
    raise Exception("Twitter exeption - Invalid confirm password", 400) 
    - Raise a validation error
    
    return user_password
    - Return the validated confirm password
"""
def validate_user_password_confirm():
    user_password = request.form.get("user_password_confirm", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password): raise Exception("Twitter exception - Invalid confirm password", 400)
    return user_password


######## VALIDATION: UUID4 ########
"""
    Validate that the string is a valid UUID v4.
    If no uuid4 is passed as an argument, it will try
    to read it from request.values. I don't use this one either
"""
REGEX_UUID4 = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
def validate_uuid4(uuid4 = ""):
    if not uuid4:
        uuid4 = request.values.get("uuid4", "").strip()
    if not re.match(REGEX_UUID4, uuid4): raise Exception("Twitter exception - Invalid uuid4", 400)
    return uuid4




############ SEND EMAIL ##################
def send_verify_email(receiver_email):
    try:
        # Create a gmail fullflaskdemomail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords
        # My key for the twitter: nafd zujo bklo qwnc

        # Email and password of the sender's Gmail account
        sender_email = "espi0001.dummy@gmail.com" # YOUR GMAIL HERE
        password = "nafd zujo bklo qwnc"  #APP PASSWORD HERE # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = "espi0001.dummy@gmail.com" # YOUR GMAIL HERE
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "Twitter"
        message["To"] = receiver_email
        message["Subject"] = "Congrats you have signed up!"

        # Body of the email
        body = f"""Congrats, you have signed up"""

        message.attach(MIMEText(body, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

        return "email sent"
    
    except Exception as ex:
        pass
    finally:
        pass