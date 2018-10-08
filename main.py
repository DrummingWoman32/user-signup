from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

#left off at following server-side validation video tips at 7:03 in video
#left off at checking if everything was okay
#left off at email validation needing improvement because the app doesn't tell me what I did wrong if I type in a bad email

@app.route("/validate-login", methods=['POST'])
def validate():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    vp_error = ''
    email_error = ''

    #if any of the mandatory fields are empty (username checked 
    # later in code):

    if password == "" :
        password_error = "Not a valid password"

    if verify_password == "":
        vp_error = "Passwords don't match up"

    #go through username and check for spaces

    for c in username:
        if c == " " :
            username_error = "Spaces are not allowed in usernames"
            password = ""
            verify_password = ""
            break
    
    if len(username) < 3 or len(username) > 20:
        username_error = "Username must be 3 - 20 characters long"
        password = ""
        verify_password = ""
        

    if password != verify_password:
        vp_error = "Passwords don't match up"
        verify_password = ""
        password = ""

    #go through password and check for spaces

    spaces = 0

    if len(password) < 3 or len(password) > 20:
        password_error = "Passwords must be 3 to 20 characters long"
        password = ""
        verify_password = ""

    else:
        for c in password:
            if c == " ":
                spaces += 1

    if spaces != 0:
        password_error = "Spaces are not allowed in passwords"
        password = ""
        verify_password = ""

    #go through email and check for anything inappropriate

    amount_of_a = 0
    amount_of_pers = 0
    email_spaces = 0

    if email != "":

        for c in email:
            if c == '@':
                amount_of_a += 1
        
            if c == '.':
                amount_of_pers += 1

            if c == ' ':
                email_spaces += 1

        if amount_of_a != 1 or amount_of_pers != 1 or len(email) < 3 or len(email) > 20 or email_spaces != 0:
            email_error = "Invalid email: must have only one @, one ., no spaces, and must be between 3 to 20 characters long"
            password = ""
            verify_password = ""

    #rendering the needed template in the end...
        
    if username_error == "" and password_error == "" and vp_error == "" and email_error == "" :
        
        return render_template('login_confirmation.html', username=username)
        
    else:
        return render_template('base.html', username=username, password=password,
        verify_password=verify_password, email=email, username_error=username_error,
        password_error=password_error, vp_error=vp_error, email_error=email_error)
    
    

@app.route("/login_confirmation", methods=['POST'])
def welcome_page():
    username = request.form['username']
    return render_template('login_confirmation.html', username = username)


@app.route("/", methods=['GET', 'POST'])
def index():
    #encoded_error = request.args.get("error")
    #return render_template('edit.html')
    return render_template('base.html')
    #username=username, password=password, 
    #verify_password = verify_password, email=email )

app.run()