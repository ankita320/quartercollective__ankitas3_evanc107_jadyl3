# quartercollective: Ankita Saha, Evan Chan, Jady Lei
# SoftDev
# October 2024

import sqlite3

USER_FILE="users.db"

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
        c.execute("INSERT INTO users (username, password, city, wordle, streak) VALUES (?, ?, ?)", (username, password, city, 0, 0))
        users.commit()
        return
    return "Username taken"

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

def deleteUsers():
    db = sqlite3.connect(USER_FILE) 
    c = db.cursor()
    c.execute("DROP table users")