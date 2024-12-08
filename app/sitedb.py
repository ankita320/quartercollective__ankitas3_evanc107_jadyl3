# quartercollective: Ankita Saha, Evan Chan, Jady Lei
# SoftDev
# October 2024

import sqlite3

USER_FILE="databse.db"

# USER DATABASE FUNCTIONS------------------------------------------------------------------------------------------------
# edit data
def createUsers():
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, city TEXT, wordle INTEGER, streak INTEGER)"
    c.execute(command)
    users.commit()

def addUser(username, password, city):
    users = sqlite3.connect(USER_FILE)
    goodcharas = set("abcdefghijklmnop12345678910.ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if set(username).difference(goodcharas) or set(password).difference(goodcharas):
        return "There are special characters in the username or password."
    c = users.cursor()
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO users (username, password, city, wordle, streak) VALUES (?, ?, ?, ?, ?)", (username, password, city, 0, 0))
        users.commit()
        return
    return "Username taken."

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
    c.execute("SELECT city FROM users WHERE username=?", (username))
    if c.fetchone() == None:
        return False
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    res = c.fetchone()
    if (password != res[0]):
        return "Invalid login; please try again."
    return True

def returnCity(username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT city FROM users WHERE username=?", (username))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]

# dev stuff
def returnEntireUsersTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users")
    return c.fetchall()

def deleteUsers():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table users")

#WEBSITE DATABASE ----------------------------------------------------------------------------------------
# create data entries
def createWebsiteInfo():
    webinfo = sqlite3.connect(USER_FILE)
    c = webinfo.cursor()
    command = "CREATE TABLE IF NOT EXISTS webinfo (username TEXT, wordOfTheDay TEXT, temperature TEXT, conditions TEXT"
    c.execute(command)
    webinfo.commit()

def enterUserInfo(username):
    webinfo = sqlite3.connect(USER_FILE)
    c = webinfo.cursor()
    c.execute("INSERT INTO webinfo (username) VALUES (?)", (username))
    webinfo.commit()

def updateUserInfoWeather(username, temperature, conditions):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM webinfo WHERE username=?", (username))).fetchone() == None:
        return
    c.execute("UPDATE webinfo SET temperature=?, conditions=? WHERE username=?", (temperature, conditions, username))
    users.commit()

def updateWordOfTheDay(wordOfTheDay):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("UPDATE webinfo SET wordOfTheDay=?", (wordOfTheDay))
    db.commit()

#return functions
def getWord(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT wordOfTheDay FROM webinfo WHERE username=?", (username))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]

def getTemperature(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT temperature FROM webinfo WHERE username=?", (username))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]

def getWeatherConditions(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT conditions FROM webinfo WHERE username=?", (username))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]

# dev functions
def returnEntireWebinfoTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM webinfo")
    return c.fetchall()

def deleteWebinfo():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table webinfo")

#ARTICLE DATABASE ----------------------------------------------------------------------------------------
