## Quarter Collective: Ankita Saha, Evan Chan, and Jady Lei


# imports
import os
import sqlite3
import json
import urllib.request
import datetime

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


@app.route("/wordle")
def doWordle():
    return render_template("wordle.html", word = getDailyWord())

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
    session.pop('username', None)
    return redirect("/")


def city():
    if 'username' in session:
        us = session['username']
        userData = get_user_data(us)
        if userData:
            print("User data:", userData)
        else:
            print("User not founddd")
        return userData[2]

def weather_type():
    with open("keys/key_openweathermap.txt") as file:
        key = file.read().strip()
    ##conditional for key
    ##try catch/conditional if city dont exist or not spell right
    city= "london"
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    weatherDescrip = w_info["weather"][0]["main"]
    return weatherDescrip

def weather_temp():
    try:
        with open("keys/key_openweathermap.txt") as file:
          key = file.read().strip()
    except:
      print("Error: API key is missing")
      return None
    city="london"
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    temp = w_info["main"]["temp"]
    temp = int(temp * (9/5) - 459.67)
    return temp

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
    print("Current working directory:", os.getcwd())
    with open("wordbank.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    if not lines:
        return None

    n = int(datetime.datetime.now().strftime("%S"))
    index = n % len(lines)

    return lines[index]

def get_my_ip():
    return jsonify({'ip': request.remote_addr})

def dict_c_api():
    try:
        with open("keys/key_merriam_webster_c.txt") as file:
            key = file.read().strip()
    except:
        return "Key error!!!!!! api doesnt work"
    word=getDailyWord().strip()
    print(word)
    url = urllib.request.urlopen(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}")
    json_d = url.read()
    try:
        info = json.loads(json_d.strip())
    except:
        return {"error!!!!!!!!!!!!!1!!!"}
    try:
        word_def = info[0]["def"][0]["sseq"][1][0][1]["dt"][0][1]
        if "|" in word_def:
            word_def = info[0]["def"][0]["sseq"][0][0][1]["dt"][0][1]
        word_def = word_def.replace("sx", " ")
        word_def=word_def.replace("{bc}", " ")
        word_def=word_def.replace("{it}", " ")
        word_def=word_def.replace("{/it}", " ")
        return word_def
    except:
        try:
            word_def = info[0]["def"][0]["sseq"][0][0][1]["dt"][0][1]
            if "|" in word_def:
                word_def = info[0]["def"][0]["sseq"][1][0][1]["dt"][0][1]
            word_def=word_def.replace("sx", " ")
            word_def=word_def.replace("{it}", " ")
            word_def=word_def.replace("{/it}", " ")
            return word_def
        except:
            try:
                word_def = info[0]["def"][0]["sseq"][0][0][1]["sense"]["dt"][0][1]
                word_def=word_def.replace("sx", " ")
                word_def=word_def.replace("{bc}", " ")
                return word_def
            except:
                try:
                    word_def = info[0]["shortdef"][0]
                    word_def=word_def.replace("sx", " ")
                    word_def=word_def.replace("{bc}", " ")
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
    if weather_type() == "Rain":
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
    city= "city"

    with open("keys/key_NYT.txt") as file:
        key = file.read().strip()

    if len(getArticles("rain")) == 0:
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
                pub_date += l
            snippet = i["snippet"]
            hearts = 16
            web_url = i["web_url"]
            createArticleEntry("rain", headline, pub_date, snippet, hearts, web_url)
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

    return render_template("home.html", main_articles=main_articles, weather_T=weather_T, tmp = tmp, w=w, city=city)



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
