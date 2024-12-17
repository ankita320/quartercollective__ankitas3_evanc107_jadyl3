## Quarter Collective: Ankita Saha, Evan Chan, and Jady Lei


# imports
import os
import sqlite3
import json
import urllib.request
import datetime
import random

from flask import Flask, render_template, redirect, session, request, flash, jsonify

#custom module
from sitedb import *
from wordle import *


# flask App
app = Flask(__name__, template_folder = "templates", static_folder = "../static")
app.secret_key = os.urandom(32)

@app.route("/")# checks for session and sends user to appropriate spot
def checkSession():
    createUsers()
    # reset(getDailyWord().upper())
    if 'username' in session:
        return redirect("/home")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])# will code registering and logging forms later
def login():
    if 'username' in session:
        return redirect("/home")

    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:# checks if both form entries were filled out
            flash("Missing username/password", "error")
            return redirect("/login")

        if checkPassword(username, password):# if password is correct, given user exists
            session["username"] = username# adds user to session
            return redirect("/home")

        else:# if password isnt correct
            flash("Invalid username/password", "error")
            return redirect("/login")

    return render_template("login.html")# if GET request, just renders login page

@app.route("/register", methods=["GET", "POST"])# will code registering and logging forms later
def register():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        city = request.form.get("city")

        if not username or not password or not city:# checks if all 3 form entries were filled out
            return render_template("register.html", warning = "empty field(s)")

        #check if user has special chars
        #check for existing username
        message = addUser(username, password, city)
        if message:
            return render_template("register.html", warning = message)
        else:
            return redirect("/login")

    return render_template("register.html")


@app.route("/wordle", methods=["GET", "POST"])
def wordle():
    global board, juvieBoard, boardPos, currGuess, guessPos, answer
    if 'username' not in session:
        return redirect("/home")

    if 'board' not in session:
        print('reset!!')
        session['board'] = [['_' for _ in range(letterPerWord)] for _ in range(guessesPerGame)]
        session['juvieBoard'] = session['board'].copy()
        session['boardPos'] = 0
        session['currGuess'] = ['_' for _ in range(letterPerWord)]
        session['guessPos'] = 0
        session['answer'] = getDailyWord().upper()

    else:
        session['board'] = board
        session['juvieBoard'] = juvieBoard
        session['boardPos'] = boardPos
        session['currGuess'] = currGuess
        session['guessPos'] = guessPos
        session['answer'] = getDailyWord().upper()

    board = session['board']
    print('session: ', board)
    juvieBoard = session['juvieBoard']
    boardPos = session['boardPos']
    currGuess = session['currGuess']
    guessPos = session['guessPos']
    answer = getDailyWord().upper()

    if request.method == "POST":
        user_guess = request.form.get("guess").upper()

        board[boardPos] = list(user_guess)
        boardPos+=1
        addGuess(user_guess)
        enterGuess()
        juvieBoard = policeGuess()

        print(board)
        print(juvieBoard)
        if user_guess == answer:
            return render_template("wordle.html", boardd = board, juvie_board = juvieBoard, win = True, answer = getDailyWord().upper(), lpw = letterPerWord, gpg = guessesPerGame, bp = boardPos)

    return render_template("wordle.html", boardd = board, juvie_board = juvieBoard, win = False, answer = getDailyWord().upper(), lpw = letterPerWord, gpg = guessesPerGame, bp = boardPos)

@app.route('/user')
def selfProfile():
    if 'username' in session:
        us =  session['username']
        return redirect('/user/'+us)

@app.route("/user/<user_id>")# viewing individual users
def profile(user_id):
    if 'username' in session:
        us = session['username']
        userData = get_user_data(us)

        if userData:
            print("User data:", userData)
        else:
            print("User not founddd")
    else:
        return redirect ('/')
    return render_template('user.html', cUser = us, city = userData[2])

def get_user_data(username):
    db = sqlite3.connect(USER_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    userData = c.fetchone()
    db.close()
    return userData


@app.route("/article/<int:post_id>")# viewing news posts
def view_article(post_id):
    return render_template('post.html')


@app.route("/logout")
def removeSession():
    session.pop('board', None)
    session.pop('juvieBoard', None)
    session.pop('boardPos', None)
    session.pop('currGuess', None)
    session.pop('guessPos', None)
    session.pop('answer', None)
    session.pop('username', None)
    return redirect("/")


def city():
    if 'username' in session:
        us = session['username']
        userData = get_user_data(us)
        if userData:
            print("User data:", userData)
            return userData[2]
        else:
            print("User not founddd")
        return userData[2]
    else:
        return "not logged in"

def weather_type():
    with open("keys/key_openweathermap.txt") as file:
        key = file.read().strip()
    ##conditional for key
    ##try catch/conditional if city dont exist or not spell right
    city_r=city().strip()
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city_r}&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    weatherDescrip = w_info["weather"][0]["main"] # gets the different weather conditions (rain, cloudy, hazy)
    return weatherDescrip

def weather_temp():
    with open("keys/key_openweathermap.txt") as file:
      key = file.read().strip() #ensures that there are no other characters that might be causing issues to code    
    city_r=city().strip()
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city_r}&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    temp = w_info["main"]["temp"] #gets the weather temo in kelvin
    temp = int(temp * (9/5) - 459.67) # converts to farenheit
    return temp

def weather_icon():
    with open("keys/key_openweathermap.txt") as file:
      key = file.read().strip() #ensures that there are no other characters that might be causing issues to code
    city_r=city().strip()
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city_r}&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    icon = w_info["weather"][0]["icon"] #gets the weather temo in kelvin
    return icon

# def getDailyWord():
#     with open("wordbank.txt") as file:
#         lines = file.readlines()
#     for i in lines:
#         i = i.strip()
#     n = int(datetime.datetime.now().strftime("%S"))
#     print(n)
#     # word = ""
#     # for i in n:
#     #     word += i
#     for num in range(0,len(lines)):
#         if (n == 0):
#             f = n
#             print(n)
#             fin = lines[num]
#             num+=1
#             n = int(datetime.datetime.now().strftime("%S"))
#             if (n > f):
#                 return lines[num]
#             else:
#                 num +=0
#         else:
#             word = lines[num]
#             print(num)
#             num+=1
#             return lines[num]

def getDailyWord():
    with open("wordbank.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    if not lines:
        return None

    # n = int(datetime.datetime.now().strftime("%S")) #gets the day of the month (someone fix this so its the day of the month and not the current sefcond)
    # index = n % len(lines) #gets a new word by using the day of the month to get the word at that index number


    random.seed(datetime.datetime.now().strftime("%m%d%Y"))
    return lines[random.randint(0, 999)]

def get_my_ip():
    return jsonify({'ip': request.remote_addr})

def dict_c_api():
    with open("keys/key_merriam_webster_c.txt") as file:
            key = file.read().strip()
     #tweaking
    word=getDailyWord().strip()
    # print(word)
    url = urllib.request.urlopen(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}")
    json_d = url.read()
    try:
        info = json.loads(json_d.strip())
    except:
        return {"error!!!!!!!!!!!!!1!!!"}
    try:
        word_def = info[0]["def"][0]["sseq"][1][0][1]["dt"][0][1] #so there's a lot of different exeptions.. # gets the diffention of the word
        if "|" in word_def:
            word_def = info[0]["def"][0]["sseq"][0][0][1]["dt"][0][1] #often the first def is the correct and often the second def is the correct, so if statements are accounting for those by checking which ones have special characters
        word_def = word_def.replace("sx", " ")
        word_def=word_def.replace("{bc}", " ")
        word_def=word_def.replace("{it}", " ")
        word_def=word_def.replace("{/it}", " ")
        word_def=word_def.replace("{d_link|", " ")
        return word_def
    except:
        try:
            word_def = info[0]["def"][0]["sseq"][0][0][1]["dt"][0][1]
            if "|" in word_def:
                word_def = info[0]["def"][0]["sseq"][1][0][1]["dt"][0][1]
            word_def=word_def.replace("sx", " ")
            word_def=word_def.replace("{it}", " ")
            word_def=word_def.replace("{bc}", " ")
            word_def=word_def.replace("{/it}", " ")
            word_def=word_def.replace("{d_link|", " ")
            return word_def
        except:
            try:
                word_def = info[0]["def"][0]["sseq"][0][0][1]["sense"]["dt"][0][1]
                word_def=word_def.replace("sx", " ")
                word_def=word_def.replace("{bc}", " ")
                word_def=word_def.replace("{it}", " ")
                word_def=word_def.replace("{/it}", " ")
                word_def=word_def.replace("{d_link|", " ")

                return word_def
            except:
                try:
                    word_def = info[0]["shortdef"][0]
                    word_def=word_def.replace("sx", " ")
                    word_def=word_def.replace("{bc}", " ") #all of the replace variables replace the special characters not part of the definition with nothing so clearer text shows up
                    word_def=word_def.replace("{it}", " ")
                    word_def=word_def.replace("{/it}", " ")
                    word_def=word_def.replace("{d_link|", " ")
                    return word_def
                except:
                    return "word not found"

@app.route("/home")
def NYT_api():
    if 'username' not in session:
        return redirect('/')
    createArticleDB()
    # key = None
    #key = 'LSAtMXzQ7AkqoSHVXfNoHpX9JuGOBtUi'
    if weather_type() == "Rain":  #gets the api content for weather type and creates variable to show on website
        weather_T = "rainy"
    elif weather_type() == "Snow":
        weather_T = "snowy"
    elif weather_type() == "Clear":
        weather_T = "sunny"
    elif weather_type() == "Clouds":
        weather_T = "cloudy"
    else:
        weather_T = "hazy"
    w = ""
    tmp = 0
    city_r=city().strip()
    icon = weather_icon()

    with open("keys/key_NYT.txt") as file:
        key = file.read().strip()

    if len(getArticles("rain")) == 0: #getting articles based on main weather condition (articles about rain to rain articles, sunny to sunny etc.)
        rain_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=rain&api-key={key}")
        rainArticles = []
        json_d = rain_url.read()
        info = json.loads(json_d.strip())

        for i in info["response"]["docs"]:
            headline = i["headline"]["main"]
            pub_date = ""
            for l in i["pub_date"]:
                if l == "T":
                    break
                pub_date += l  #gets just the date of the article and no other information
            snippet = i["snippet"]
            hearts = 16
            web_url = i["web_url"]
            createArticleEntry("rain", headline, pub_date, snippet, hearts, web_url) #creates request to api for the first time to store it in the variable so that every other time, it only uses the database and not the api w constant request
    else:
        rain_Articles = getArticles("rain")


    try:
        if len(getArticles("snow")) == 0:
            snow_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=snow&api-key="+key)
            snowArticles = []
            json_d = snow_url.read()
            info = json.loads(json_d.strip())

            for i in info["response"]["docs"]:
                headline = i["headline"]["main"]
                pub_date = ""
                for l in i["pub_date"]:
                    if l == "T":
                        break
                    pub_date += l
                snippet = i["snippet"]
                hearts = 16
                web_url = i["web_url"]
                createArticleEntry("snow", headline, pub_date, snippet, hearts, web_url)
        else:
            snowArticles = getArticles("snow")

    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    try:
        if len(getArticles("sunny")) == 0:
            sunny_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=sunny&api-key={key}")
            sunnyArticles = []
            json_d = sunny_url.read()
            info = json.loads(json_d.strip())

            for i in info["response"]["docs"]:
                headline = i["headline"]["main"]
                pub_date = ""
                for l in i["pub_date"]:
                    if l == "T":
                        break
                    pub_date += l
                snippet = i["snippet"]
                hearts = 16
                web_url = i["web_url"]
                createArticleEntry("sunny", headline, pub_date, snippet, hearts, web_url)
        else:
            sunnyArticles = getArticles("sunny")
            #print(main_Articles)
    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    try:
        if len(getArticles("cloudy")) == 0:
            cloudy_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=cloudy&api-key={key}")
            cloudyArticles = []
            json_d = cloudy_url.read()
            info = json.loads(json_d.strip())

            for i in info["response"]["docs"]:
                headline = i["headline"]["main"]
                pub_date = ""
                for l in i["pub_date"]:
                    if l == "T":
                        break
                    pub_date += l
                snippet = i["snippet"]
                hearts = 16
                web_url = i["web_url"]
                createArticleEntry("cloudy", headline, pub_date, snippet, hearts, web_url)
        else:
            cloudyArticles = getArticles("cloudy")

    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    try:
        if len(getArticles("hazy")) == 0:
            hazy_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=hazy&api-key={key}")
            hazyArticles = []
            json_d = hazy_url.read()
            info = json.loads(json_d.strip())

            for i in info["response"]["docs"]:
                headline = i["headline"]["main"]
                pub_date = ""
                for l in i["pub_date"]:
                    if l == "T":
                        break
                    pub_date += l
                snippet = i["snippet"]
                hearts = 16
                web_url = i["web_url"]
                createArticleEntry("hazy", headline, pub_date, snippet, hearts, web_url)
        else:
            hazyArticles = getArticles("hazy")

    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    if weather_type() == "Rain":
        main_articles = rainArticles
    elif weather_type() == "Snow":
        main_articles = snowArticles
    elif weather_type() == "Clear":
        main_articles = sunnyArticles
    elif weather_type() == "Clouds":
        main_articles = cloudyArticles
    else:
        main_articles = hazyArticles
    w = dict_c_api()
    tmp = weather_temp()

    return render_template("home.html", main_articles=main_articles, weather_T=weather_T, tmp = tmp, w=w, city=city, icon=icon)



#
# def dict_e_api():
#     file = open("keys/key_merriam_webster_e.txt")
#     key = file.read().strip()
#     if not key:
#       print("Error: API key is missing")
#       return none
#     ##conditional for key
#     url = urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/sd2/json/school?key={key}")
#     json_d = url.read()
#     info = json.loads(json_d.strip())
#     return render_template("home.html", txt=txt)
# ##function that returns user's input for city
#


if __name__ == "__main__":
    app.debug = True
    app.run()
