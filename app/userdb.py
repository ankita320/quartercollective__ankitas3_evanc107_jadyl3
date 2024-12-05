# quartercollective: Ankita Saha, Evan Chan, Jady Lei
# SoftDev
# October 2024

import sqlite3

USER_FILE="users.db"


# edit data
def createUsers():
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, city TEXT, wordle INTEGER, streak INTEGER)"
    c.execute(command)
    users.commit()

def addUser(username, password, city):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO users (username, password, city, wordle, streak) VALUES (?, ?, ?, ?, ?)", (username, password, city, 0, 0))
        users.commit()
        return
    return "Username taken"

def updateWordle(username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username))).fetchone() == None:
        return
    c.execute("SELECT streak FROM users WHERE username=?", (username,))
    streak = c.fetchone()[0]
    # print(streak)
    c.execute("UPDATE users SET wordle=?, streak=? WHERE username=?", (1, streak + 1, username))
    users.commit()

def updateDaily():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("UPDATE users SET streak=0 WHERE wordle=0")
    c.execute("UPDATE users SET wordle=0")
    db.commit()

# access information
def checkPassword(username, password):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username))).fetchone() == None:
        return "Username does not exist; please register before logging in."
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    res = c.fetchone()
    if (password != res[0]):
        return "Invalid login; please try again."
    return

def returnCity(username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT city FROM users WHERE username=?", (username))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]





def entireTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users")
    return c.fetchall()

def deleteUsers():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table users")
