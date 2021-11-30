from sqlite3 import connect
from data.table import Table

data = connect("data.db", isolation_level = None, check_same_thread=False)
users = Table(data, "users", "username")
stories = Table(data, "stories", "title")

def get_usernames():
    "retuns a list of usernames"
    return users.get_main_values()

def user_exists(username):
    "returns true if user exists"
    return users.value_exists(username)

def correct_password(username, password):
    "returns true if username matches password"
    real_password = users.get_value(username, "password")
    return password == real_password

def add_user(username, password):
    "adds a user with username and passsowrd"
    users.add_values([username, password])
    edited_stories = Table(data, username, "title")
    edited_stories.create(["title"])

def get_stories():
    return stories.get_main_values()

def get_edited_stories(username):
    "returns a list of titles of stories edited by user"
    edited_stories = Table(data, username, "title")
    return edited_stories.get_main_values()

def get_unedited_stories(username):
    "returns a list of titles of stories not edited by user"
    stories = set(get_stories())
    edited_stories = set(get_edited_stories(username))
    return stories - edited_stories

def story_exists(title):
    "returns true if story exists"
    return stories.value_exists(title)

def add_story(title):
    "adds a story with title"
    stories.add_values([title, "", ""])

def get_old_part(title):
    return stories.get_value(title, "old_part")

def get_new_part(title):
    "returns the newest addition to story"
    return stories.get_value(title, "new_part")

def attach(old_part, new_part):
    if old_part == "":
        return new_part
    return old_part + "\n\n" + new_part

def get_full_story(title):
    "returns the full text of story"
    old_part = get_old_part(title)
    new_part = get_new_part(title)
    return attach(old_part, new_part)

def add_new_part(title, new_part, username):
    "adds new part to story being edited by user"
    full_story = get_full_story(title)
    stories.set_value(title, "old_part", full_story)
    stories.set_value(title, "new_part", new_part)
    edited_stories = Table(data, username, "title")
    edited_stories.add_values([title])

def reset_data():
    "resets the database to empty user and story tables"
    open("data.db", "w").close()
    users.create(["username", "password"])
    stories.create(["title", "old_part", "new_part"])
