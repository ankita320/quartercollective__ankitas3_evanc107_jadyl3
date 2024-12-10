## Quarter Collective: Ankita Saha, Evan Chan, and Jady Lei


# imports
from flask import Flask, render_template, redirect, session, request, flash
import json
import urllib.request
import sqlite3
import os

#custom module
from sitedb import *

# flask App
app = Flask(__name__, template_folder = "templates", static_folder = "../static")
app.secret_key = os.urandom(32)

@app.route("/")# checks for session and sends user to appropriate spot
def checkSession():
    createTables()
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
        with open("keys/key_openweathermap.txt") as file:
          key = file.read().strip()
    except:
      print("Error: API key is missing")
      return none
    ##conditional for key
    ##try catch/conditional if city dont exist or not spell right
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    weatherDescrip = w_info["weather"][0]["main"]
    temp = w_info["main"]["temp"]
    return weatherDescrip

def weather_temp():
    try:
        with open("keys/key_openweathermap.txt") as file:
          key = file.read().strip()
    except:
      print("Error: API key is missing")
      return none
    ##conditional for key
    ##try catch/conditional if city dont exist or not spell right
    url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}")
    json_d = url.read()
    w_info = json.loads(json_d.strip())
    temp = w_info["main"]["temp"]
    temp = int(temp * (9/5) - 459.67)
    return temp

def dict_c_api():
    try:
        with open("keys/key_merriam_webster_c.txt") as file:
            key = file.read().strip()
    except:
        return "Key error!!!!!!"

    word = "battle"
    url = urllib.request.urlopen(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}")
    json_d = url.read()
    try:
        info = json.loads(json_d.strip())
    except:
        return {"error!!!!!"}
    print("info")
    word_def = info[0]["shortdef"][0]
    return word_def

@app.route("/home1")
def NYT_api():
    try:
        with open("keys/key_NYT.txt") as file:
            key = file.read().strip()
    except:
      print("Error: API key is missing")
      return None
    try:
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

            rainArticles.append({
                "headline": headline,
                "pub_date": pub_date,
                "snippet": snippet
            })
    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    try:
        snow_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=snow&api-key={key}")
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

            snowArticles.append({
                "headline": headline,
                "pub_date": pub_date,
                "snippet": snippet
            })

    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    try:
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

            sunnyArticles.append({
                "headline": headline,
                "pub_date": pub_date,
                "snippet": snippet
            })
    except Exception as e:
        return (f"Unexpected error! Be patient pls.")

    try:
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

            cloudyArticles.append({
                "headline": headline,
                "pub_date": pub_date,
                "snippet":snippet,
                "web_url":web_url
            })
    except Exception as e:
        return (f"Unexpected key request error! Be patient pls.")

    if weather_type() == "Rain":
        main_articles = rainArticles
        weather_T = "rainy"
    elif weather_type() == "Snow":
        main_articles = snowArticles
        weather_T = "snowy"
    elif weather_type() == "Clear":
        main_articles = sunnyArticles
        weather_T = "sunny"
    elif weather_type() == "Clouds":
        main_articles = cloudyArticles
        weather_T = "cloudy"

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
