## Quarter Collective: Ankita Saha, Evan Chan, and Jady Lei


# imports
import os
import sqlite3
import json
import urllib.request

from flask import Flask, render_template, redirect, session, request, flash

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
            return redirect("/home1")

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

@app.route("/home", methods=["GET", "POST"])
def homesweethome():
    if "username" not in session:
        return redirect("/login")
    return render_template("home.html")

@app.route("/wordle")
def doWordle():
    return render_template("wordle.html")

@app.route("/user/<int:user_id>")# viewing individual users

@app.route("/article/<int:post_id>")# viewing news posts

@app.route("/logout")
def removeSession():
    session.pop('username', None)
    return redirect("/")

def weather_type():
    try:
        with open("/keys/key_openweathermap.txt") as file:
            key = file.read().strip()
    except FileNotFoundError:
        print("Error: API key file not found")
        return None
    ##conditional for key
    ##try catch/conditional if city dont exist or not spell right
    city="london"
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
    temp = temp * (9/5) - 459.67
    return temp

def dict_c_api():
    try:
        with open("keys/key_merriam_webster_c.txt") as file:
            key = file.read().strip()
    except:
        return "Key error!!!!!! api doesnt work"
    word="potato"
    #city = returnCity(username)
    url = urllib.request.urlopen(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}")
    json_d = url.read()
    try:
        info = json.loads(json_d.strip())
    except:
        return {"error!!!!!!!!!!!!!1!!!"}
    print("info")
    try:
        word_def = info[1]["shortdef"][0]
        return word_def
    except:
        return "That word is not in our dictionary"

@app.route("/home1")
def NYT_api():
    createArticleDB()
    key = None
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
    try:
        with open("keys/key_NYT.txt") as file:
            key = file.read().strip()

    except:
      print("Error: API key is missing")
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

    return render_template("home.html", main_articles=main_articles, weather_T=weather_T, tmp = tmp, w=w)



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
