"""
    app.py
    ------
    Purpose:
    - Define all the routes (signup, login, home, logout)
    - Handle the request/response flow
    - Use validators from x.py to check user input
    - Hash passwords on signup, check them on login
    - Use sessions to remember who is logged in
    - Apply @x.no_cache to prevent showing cached pages after logout

    Flow:
    1) User signs up -> we validate input, hash password and save in DB
    2) User logs in -> we fetch by email, check password hash, start session
    3) User visits /home -> only allowed if session exists
    4) User logs out -> session is cleared -> cannot go back with btweetser back button
"""
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import x 
# import send_mail
import time
import uuid
import os

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)

# Set the maximum file size to 1 MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024   # 1 MB

# Sessions
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


##############################
##############################
##############################
def _____USER_____(): pass 
##############################
##############################
##############################


############ GET - INDEX ############
@app.get("/")
def view_index():
    return render_template("index.html")


# -------------------- LOGIN --------------------
############# GET - LOGIN view #############
@app.get("/login")
def view_login():
    if session.get("user", ""): return redirect(url_for("view_home"))

    message = request.args.get("message", "")
    return render_template("login.html", message=message)

############# POST - LOGIN handler #############
@app.post("/login")
def handle_login():
    # Login flow:
        # 1) validate email/password format
        # 2) SELECT user by email 
        # 3) Connect to the database
        # 4) compare password using check_password:hash
        # 5) create a session and redirect to /home

    try:
        # Validate
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        # Connect to the database
        q = "SELECT * FROM users WHERE user_email = %s"
        db, cursor = x.db()
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user: raise Exception("User not found", 400)

        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials", 400)

        user.pop("user_password")

        session["user"] = user
        return redirect(url_for("view_home"))

    except Exception as ex:
        ic(ex)
        if ex.args[1] == 400: return redirect(url_for("view_login", message=ex.args[0]))
        return "System under maintenance", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# -------------------- SIGNUP --------------------
############# GET - SIGNUP #############
@app.get("/signup")
def view_signup():
    message = request.args.get("message", "")
    return render_template("signup.html", message=message, x=x)

############# POST - SIGNUP #############
@app.post("/signup")
def handle_signup():
    # Sign up flow:
        # 1) read and validate the name etc
        # 2) hash the password
        # 3) INSERT user in DB inside
        # 4) commit on succes
        # 5) return clear messages + proper http status codes
    try:
        # x.validate_user_username()
        
        # return """
        # <mixhtml mix-redirect='/tweet'>
        # </mixhtml>
        # """
    

        # 1) Read and validate
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()

        # 2) hash password
        user_hashed_password = generate_password_hash(user_password)

        # Connect to the database
        # 3) INSERT user in DB 
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)"
        
        db, cursor = x.db()
        cursor.execute(q, (None, user_email, user_hashed_password, user_username, user_first_name, user_last_name, None))
        db.commit()

        receiver_email = request.form.get("user_email", "")

        # 4) Send velkomstmail
        x.send_verify_email(receiver_email=receiver_email)
        
        return redirect(url_for("view_login", message="Signup successful. Proceed to login"))
    except Exception as ex:
        ic(ex)
        if ex.args[1] == 400: return redirect(url_for("view_signup", message=ex.args[0]))
        if "Duplicate entry" and user_email in str(ex): return redirect(url_for("view_signup", message="Email already registered"))
        if "Duplicate entry" and user_username in str(ex): return redirect(url_for("view_signup", message="username already registered"))
        return "System under maintenance", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/send-email")
def send_email():
    try:
        x.send_verify_email()
        return "ok from route"
    except Exception as ex:
        ic(ex)
    finally:
        pass


# -------------------- HOME --------------------
############# GET - HOME (protected) #############
@app.get("/home")
@x.no_cache # prevents showing cached content after logout / "back" button
def view_home():
    try: 
        #user = session.get("user", "")
        #if not user: return redirect(url_for("view_login"))
        next_page = 1
        db, cursor = x.db()
        q = "SELECT * FROM users JOIN posts ON user_pk = user_fk LIMIT 0,2"
        cursor.execute(q)
        tweet = cursor.fetchall()
        ic(tweet)

        q = "SELECT * FROM trending ORDER BY RAND() LIMIT 5" 
        cursor.execute(q)
        trending = cursor.fetchall()
        ic(trending)
        
        q = "SELECT * FROM users WHERE user_pk!= 1 ORDER BY RAND() LIMIT 5" 
        cursor.execute(q)
        users_to_follow = cursor.fetchall()
        ic(users_to_follow)
        return render_template("home.html", tweet=tweet, trending=trending, users_to_follow=users_to_follow, next_page=next_page)
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

############# GET - api-get-posts #############
@app.get("/api-get-tweets")
def api_get_tweets():
    try:
        next_page = int(request.args.get("page", ""))
        ic(next_page)
        db, cursor = x.db()
        q = "SELECT * FROM users JOIN posts ON user_pk = user_fk LIMIT %s, 3"
        cursor.execute(q, (next_page*2,))
        tweet = cursor.fetchall()
        ic(tweet)

        container = ""

        for tweet in tweet[:2]:
            html_tweet = render_template("_tweet.html", tweet=tweet)
            container = container + html_tweet
            ic(container)

        if len(tweet) < 3:
            return f"""
            <mixhtml mix-bottom="#tweet">
                {container}
            </mixhtml>
            <mixhtml mix-replace="#show_more_tweets"></mixhtml>
            """
        new_hyperlink = render_template("___show_more_tweets.html", next_page=next_page+1)

        return f"""
        <mixhtml mix-bottom="#tweet">
            {container}
        </mixhtml>
        <mixhtml mix-replace="#show_more_tweets">
            {new_hyperlink}
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



# -------------------- LOGOUT --------------------
############# POST - LOGOUT #############
@app.get("/logout")
@x.no_cache # also set no-cache on logut responses
def handle_logout():
    try:
        session.clear() # clear the session so the user is logged out
        return redirect(url_for("view_login"))
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass





# -------------------- AJAX --------------------
############# GET - ajax #############
@app.get("/ajax")
def view_ajax():
    try:
        return render_template("ajax.html")
    except Exception as ex:
        return "error"
    finally:
        pass

############# GET - Tweet #############
@app.get("/tweet")
def api_tweet():
    try:
        return "You did it"
    except Exception as ex:
        return "error"
    finally:
        pass


# -------------------- AJAX POST --------------------
############# GET - ajax_post #############
@app.get("/ajax-post") # better for url with - instead of _
def view_ajax_post():
    try:
        return render_template("ajax_post.html")
    except Exception as ex:
        return "error"
    finally:
        pass


############# POST - save #############
@app.post("/save")
def api_save():
    try:
        user_name = request.form.get("user_name", "give me a name") # a variable called user_name (just like const username =)
        user_last_name = request.form.get("last_name", "")
        user_nick_name = request.form.get("nick_name", "")

        # Dictionary in Python is JSON in JavaScript
        user = {
            "user_name" : user_name.title(), # key = "user_name" with the value = user_name
            "user_last_name" : user_last_name.upper(), # makes everything capital
            "user_nick_name" : user_nick_name.title()  # makes the first letter capital
        }

        return user
    except Exception as ex:
        return "error"
    finally:
        pass



# -------------------- AJAX HEART --------------------
############# GET - ajax_heart #############
@app.get("/ajax-heart") 
def view_ajax_heart():
    try:
        return render_template("ajax_heart.html")
    except Exception as ex:
        return "error"
    finally:
        pass


############# GET - Like tweet #############
@app.get("/api-like-tweet")
def api_like_tweet():
    try:
        # TODO: Validate the data
        # TODO: Get the logged user id 
        # TODO: Connect to the database
        # TODO: Disconnect to the database
        # TODO: Insert the liking of a tweet in the table
        # TODO: Check that everything went as expected
        # TODO: Reply to the browser information that the tweet has been liked

        #return a json object -> a Dictionary
        return {"status":"ok"}
    except Exception as ex:
        return {"status":"error"} # can pass a 400 or 500
    finally:
        pass


############# GET - Unlike tweet #############
@app.get("/api-unlike-tweet")
def api_unlike_tweet():
    try:
        # TODO: Validate the data
        # TODO: Get the logged user id 
        # TODO: Connect to the database
        # TODO: Disconnect to the database
        # TODO: Delete the liking of a tweet in the table
        # TODO: Check that everything went as expected
        # TODO: Reply to the browser information that the tweet has been liked

        #return a json object -> a Dictionary
        return {"status":"ok"}
    except Exception as ex:
        return {"status":"error"} # can pass a 400 or 500
    finally:
        pass



# -------------------- AJAX Bookmark --------------------
############# GET - ajax_bookmark.html #############
@app.get("/ajax-bookmark") 
def view_ajax_bookmark():
    try:
        return render_template("ajax_bookmark.html")
    except Exception as ex:
        return "error"
    finally:
        pass


############# POST - api_bookmark #############
@app.post("/api-bookmark") 
def api_bookmark():
    try:
        # connect to the database, validate ect.
        return """
        <mixhtml mix-replace='button'>
            <button mix-post="/api-remove-bookmark">
                <i class="fa-solid fa-bookmark"></i>
            </button>
        </mixhtml>
        <mixhtml mix-before='button'>
            <div mix-ttl="5000" mix-fade-out>
                I will disappear
            </div>
        </mixhtml>
        """
    except Exception as ex:
        return "error"
    finally:
        pass



# -------------------- ITEMS --------------------
############# GET - items.html #############
@app.get("/items") 
def view_items():
    try:
        next_page = 1
        db, cursor = x.db()
        q = "SELECT * FROM posts LIMIT 0,2"
        cursor.execute(q) # we dont need a tuple because we dont have any placeholders
        items = cursor.fetchall()
        ic(items) # showing the items in the terminal
        return render_template("items.html", items=items, next_page=next_page) # passing the items though the website 
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



############# GET - api-get-items #############
@app.get("/api-get-items") 
def api_get_items():
    try:
        next_page = int(request.args.get("page", "")) # we need to grab the variable from the url -> its the page 2 # make it a number, therefore the int() function
        ic(next_page)
        db, cursor = x.db()
        q = "SELECT * FROM posts LIMIT %s, 3" # has to be the new number
        cursor.execute(q, (next_page*2,)) 
        items = cursor.fetchall()
        ic(items)
    
        container = "" # create a empty box

        for item in items[:2]: #plane python loop
            html_item = render_template("_item.html", item=item) #create a html for the item component
            container = container + html_item # put the html in the empty box
            ic(container)
        
        if len(items) < 3:
            return f"""
            <mixhtml mix-bottom="#items">
                {container}
            </mixhtml>
            <mixhtml mix-replace="#show_more"></mixhtml>
            """

        new_hyperlink = render_template("___show_more.html", next_page=next_page+1)
        
        return f"""
        <mixhtml mix-bottom="#items">
            {container}
        </mixhtml>
        <mixhtml mix-replace="#show_more">
            {new_hyperlink}
        </mixhtml>
        
        """
        

        
        # return render_template("items.html", items=items) 
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


