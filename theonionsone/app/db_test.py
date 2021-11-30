from data.data_functions import *

def username_test(username):
    if user_exists(username):
        no = ""
    else:
        no = " NOT"
    print(f"{username} is{no} a user")

def story_test(title):
    if story_exists(title):
        no = ""
    else:
        no = " NOT"
    print(f"{title} is{no} a story")

def password_test(username, password):
    if correct_password(username, password):
        no = ""
    else:
        no = " NOT"
    print(f"{password} is{no} the correct password for {username}")

def show_new_part(title):
    new_part = get_new_part(title)
    print(f"most recent part of {title} is:\n\"\n{new_part}\n\"")

def show_full_story(title):
    full_story = get_full_story(title)
    print(f"the entirety of {title} is:\n\"\n{full_story}\n\"")

def show_edited_stories(username):
    edited_stories = list(get_edited_stories(username))
    print(f"{username} has edited: {edited_stories}")

def show_users():
    usernames = list(get_usernames())
    print(f"all users: {usernames}")

def show_stories():
    titles = list(get_titles())
    print(f"all stories: {titles}")

reset_data()

add_user("bob", "goodpassword")
add_user("joe", "okaypassword")
username_test("bob")
username_test("joe")
username_test("carlos")
add_user("carlos", "coolpassword")
password_test("bob", "goodpassword")
password_test("joe", "okaypassword")
password_test("bob", "idk")

add_story("harry potter")
add_new_part("harry potter", "there once was a boy named harry", "bob")
add_new_part("harry potter", "he did stuff at school", "carlos")
add_story("lord of the rings")
add_new_part("lord of the rings", "frodo baggins liked submarines", "joe")
add_new_part("lord of the rings", "he sailed through the oceans", "carlos")
add_new_part("lord of the rings", "he sailed through all the streams", "bob")
show_new_part("lord of the rings")
show_full_story("lord of the rings")
story_test("harry potter")
story_test("lord of the rings")
story_test("cheese")
show_users()
show_stories()
show_edited_stories("bob")
show_edited_stories("joe")
show_edited_stories("carlos")
