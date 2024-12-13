# quartercollective: Ankita Saha, Evan Chan, Jady Lei
# SoftDev
# October 2024

import sqlite3

USER_FILE="databse.db"

def createTables():
    createUsers()
    createArticleDB()
    createWebsiteInfo()
    createWordleGuessTable()
    createNotesTable()

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
    goodcharas = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345678910._-")
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
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
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
    c.execute("SELECT city FROM users WHERE username=?", (username,))
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
    c.execute("SELECT city FROM users WHERE username=?", (username,))
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
    c.execute("INSERT INTO webinfo (username) VALUES (?)", (username,))
    webinfo.commit()

def updateUserInfoWeather(username, temperature, conditions):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM webinfo WHERE username=?", (username,))).fetchone() == None:
        return
    c.execute("UPDATE webinfo SET temperature=?, conditions=? WHERE username=?", (temperature, conditions, username))
    users.commit()

def updateWordOfTheDay(wordOfTheDay):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("UPDATE webinfo SET wordOfTheDay=?", (wordOfTheDay,))
    db.commit()

#return functions
def getWord(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT wordOfTheDay FROM webinfo WHERE username=?", (username,))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]

def getTemperature(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT temperature FROM webinfo WHERE username=?", (username,))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchone()[0]

def getWeatherConditions(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT conditions FROM webinfo WHERE username=?", (username,))
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

#ARTICLE DATABASE ------------------------------------------------------------------------------------
# create article entries
def createArticleDB():
    articles = sqlite3.connect(USER_FILE)
    c = articles.cursor()
    command = "CREATE TABLE IF NOT EXISTS articles (weathercondition TEXT, articlename TEXT, date TEXT, synopsis TEXT, hearts INTEGER, url TEXT)"
    c.execute(command)
    articles.commit()

def createArticleEntry(weathercondition, articlename, date, synopsis, hearts, url):
    articles = sqlite3.connect(USER_FILE)
    c = articles.cursor()
    c.execute("INSERT INTO articles (weathercondition, articlename, date, synopsis, hearts, url) VALUES (?, ?, ?, ?, ?, ?)", (weathercondition, articlename, date, synopsis, hearts, url))
    articles.commit()

def updateHearts(weathercondition, articlename, change):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT hearts FROM articles WHERE articlename=? AND weathercondition=?", (articlename, weathercondition))
    newHearts = c.fetchone()[0] + change
    c.execute("UPDATE articles SET hearts=? WHERE articlename=? AND weathercondition=?", (newHearts, articlename, weathercondition))
    users.commit()

#return functions
def getArticle(weathercondition, articlename):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM articles WHERE articlename=? AND weathercondition=?", (articlename, weathercondition))
    return c.fetchone()[0]

def getArticles(weathercondition):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM articles WHERE weathercondition=?", (weathercondition, ))
    return c.fetchall()

# dev functions
def returnEntireArticleTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM articles")
    return c.fetchall()

def deleteArticles():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table articles")

# WordleGuessTable -------------------------------------------------------------------------------------------------
# create and edit table
def createWordleGuessTable():
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    command = "CREATE TABLE IF NOT EXISTS wordleGuesses (username TEXT, date TEXT, guess Text)"
    c.execute(command)
    users.commit()
def addGuess(username, date, guess):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("INSERT INTO wordleGuesses (username, date, guess) VALUES (?, ?, ?)", (username, date, guess))
# access information
def returnGuesses(username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT guess FROM wordleGuesses WHERE username=?", (username,))
    if c.fetchone() == None:
        return "No such user"
    else:
        return c.fetchall()
# dev stuff
def returnEntireGuessesTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM wordleGuesses")
    return c.fetchall()
def deleteGuesses():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table wordleGuesses")

# NotesTable -------------------------------------------------------------------------------------------------
# create and edit table
def createNotesTable():
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    command = "CREATE TABLE IF NOT EXISTS notes (username TEXT, articlename TEXT, date TEXT, note Text)"
    c.execute(command)
    users.commit()

def addNote(username, articlename, date, note):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("INSERT INTO notes (username, articlename, date, note) VALUES (?, ?, ?, ?)", (username, articlename, date, note))

# access information
def returnNote(username, articlename):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT date, note FROM notes WHERE username=? AND articlename=?", (username, articlename))
    if c.fetchone() == None:
        return "No such note"
    else:
        return list(c.fetchall())

def returnNotes(articlename):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT date, note FROM notes WHERE articlename=?", (articlename, ))
    if c.fetchone() == None:
        return "No such notes"
    else:
        return list(c.fetchall())

def returnNotesNum(articlename):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT date, note FROM notes WHERE articlename=?", (articlename, ))
    if c.fetchone() == None:
        return "No such note"
    else:
        return list(c.fetchall())
# dev stuff
def returnEntireNotesTable():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM notes")
    return c.fetchall()
def deleteNotes():
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("DROP table notes")
    
