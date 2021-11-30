from flask import session
from flask import request, render_template, Flask, redirect
from data.data_functions import *
from os import urandom
app = Flask(__name__)
debug = True
#why do we need secret keys? For this project it is not really necessary but...
#https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key
#I believe in a real life environment we should store the key somewhere safe in case of server crash
app.secret_key = urandom(24)
#   Things to work on:
#   Implimentationationation
#   Adding error messages and try and fails

#helper method
def unauthorizedFlow():
    '''
    returns static html for when user accesses site they should not
    '''

    #simply redirects to desired site
    return redirect("/static/unauthorized.html", code=302)

#helper method
def userSignedIn():
    '''
    returns the status of user login
    '''
    return 'username' in session.keys() and session['username']

@app.route("/", methods=['GET', 'POST'])
def welcome():
    '''
    Welcome Page
    '''
    try:

        if userSignedIn():
            return render_template("home_Page.html", user = session['username'])

        else:
            return render_template('login_Page.html')
    except:
        return render_template('ErrorResponse.html')

@app.route("/register", methods=['GET', 'POST'])
def disp_registerpage():
    '''
    register page
    '''
    try:
        if userSignedIn():
            return unauthorizedFlow()

        return render_template('register.html')
    except:
        return render_template('ErrorResponse.html')

#Checks the register to make sure everything is good
#Password and confirm password should be the same
@app.route("/check_register", methods=['GET', 'POST'])
def check_register():
    '''
    function for post-form request; register process given POST form arguments
    '''

    try:
        if userSignedIn():
            return unauthorizedFlow()

        #store form information
        username = request.form.get('username')
        password = request.form.get('password')
        con_password = request.form.get('confirm_password')

        #checks password requirements against password confirmation and password existence; False means it passes requirements
        password_conflict = (not bool(password)) or password != con_password

        #checks db for existing user and user existence; False means it passes requirements
        username_conflict = (not bool(username)) or user_exists(username)

        if not (password_conflict or username_conflict):
            add_user(username,password)
            return render_template('login_Page.html', extra_Message="Successfully Registered")

        else:
            #Error messages based on incorrect input types
            extra_Message = "An error has been made trying to register you."
            if password_conflict:
                extra_Message = "Password requirements not met. Check to see that password is at least one character and that password confirmation matches"

            elif username_conflict:
                extra_Message = "Username may already be in use, or does not contain at least one character"

            return render_template('register.html', extra_Message=extra_Message)
    except:
        return render_template('ErrorResponse.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    '''
    logs out the user by setting 'username' key to None
    '''

    try:
        session['username'] = None
        return render_template('login_Page.html', extra_Message="Successfully Logged Out")
    except:
        return render_template('ErrorResponse.html')

@app.route("/auth_ed", methods=['POST'])
def authenticate():
    '''
    authorization page; redirects and logs in if credentials work, loads login template if not
    '''
    try:
        #retrieve from FORM instead of ARGS because we are retrieving from POST method
        username = request.form.get('username')
        password = request.form.get('password')

        #authflow variable
        loginAuthorized = user_exists(username) and correct_password(username,password)

        if loginAuthorized:
            session['username'] = username
            return redirect("/", code = 302)
        else:
            return render_template('login_Page.html', extra_Message="Login failed, please try again")

    except:
        return render_template('ErrorResponse.html')

@app.route("/your_stories", methods=['GET', 'POST'])
def your_Story():
    '''
    provides the user with the list of stories they contributed to
    '''
    if not userSignedIn():
        return unauthorizedFlow()
    try:
        user_stories = get_edited_stories(session['username']) #returns the output of map
        #this output of map is disposable, so after iterating through and using the object its contents get removed

        if(userSignedIn()):
            return render_template('your_Stories.html', stories = list(user_stories), verb = "'ve")
        else:
            return unauthorizedFlow()

    except:
        return render_template('ErrorResponse.html')

@app.route("/stories", methods=['GET', 'POST'])
def stories():
    '''
    returns a list of all stories that exist
    '''
    try:
        unedited_stories = get_unedited_stories(session['username']) # returns the output of map
        #this output of map is disposable, so after iterating through and using the object its contents get removed

        if(userSignedIn()):
            return render_template('your_Stories.html', stories=list(unedited_stories), verb = " haven't")
        else:
            return unauthorizedFlow()

    except:
        return render_template('ErrorResponse.html')

@app.route("/stories/<string:title>")
def getStory(title):
    '''
    returns story <title>
    '''
    if not userSignedIn():
        return unauthorizedFlow()

    try:
    #utilizes the title variable found in the url and inputs it into the template, along with the content needed to be retrieved
        user_stories = get_edited_stories(session['username'])

        #https://stackoverflow.com/questions/12244057/any-way-to-add-a-new-line-from-a-string-with-the-n-character-in-flask
        if (title in user_stories): #different depending on whether user has editted the story
            return render_template("story.html", story = title, contents = get_full_story(title).split("\n"))
            #return get_full_story(title)
        else:

            return render_template("see_story.html", story=title, latest_contents = get_new_part(title).split("\n"))
            #return get_full_story(title)

    except:
        return render_template('ErrorResponse.html')

@app.route("/createstory" , methods = ['GET', 'POST'])
def create_story():
    '''
    provides UI for creating a story
    '''

    try:
        if(not userSignedIn()):
            return unauthorizedFlow()

        return render_template('create_New.html', user = session['username'])
    except:
        return render_template('ErrorResponse.html')

@app.route("/requestcreate", methods = ["GET","POST"])
def requestCreate():
    '''
    creates the desired story if requirements are met
    '''
    try:
        if(not userSignedIn()):
            return unauthorizedFlow()

        title = request.form.get('title')
        contents = request.form.get('story')

        matchedRequirements = not story_exists(title)

        if matchedRequirements:
            if debug:
                print (user_exists(session['username']))
                print("Requirements Met. Creating story")

                add_story(title)
                print("Story created")

                add_new_part(title,contents,session['username'])
                print("Contents added")

                print("Was the story added to db? " + str(story_exists(title)))
                print("Contents of the story: " + get_full_story(title))
            else:

                add_story(title)
                add_new_part(title, contents, session['username'])
        else:
            return render_template("create_New.html", user = session['username'], error = True)

        return redirect("/your_stories")

    except:
        return render_template('ErrorResponse.html')

@app.route("/edit_Story/<string:title>", methods = ["GET","POST"])
def edit_Story(title):
    try:
        if not userSignedIn():
            return unauthorizedFlow()

        return render_template("edit_Story.html", story = title, latest_contents = get_new_part(title))
    except:
        return render_template('ErrorResponse.html')

@app.route("/requestaddition/<string:title>", methods = ["GET", "POST"])
def requestAddition(title):
    try:
        if(not userSignedIn()):
            return unauthorizedFlow()
        new_contents = request.form.get('story')
        new_content = "\n" + new_contents
        add_new_part(title, new_contents, session['username'])
        return redirect("/your_stories")
    except:
        return render_template('ErrorResponse.html')

def main():
    """
    false if this file imported as module
    debugging enabled
    """
    try:
        app.debug = True
        app.run(host = '0.0.0.0')
    except:
        return render_template('ErrorResponse.html')

if __name__ == "__main__":
    main()