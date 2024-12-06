### Quarter Collective: Ankita Saha, Evan Chan, and Jady Lei


# imports
from flask import Flask, render_template, redirect, session, request, flash
import json
import urllib.request
import sqlite3
import os

# flask App
app = Flask(__name__, template_folder = "templates", static_folder = "../static")
app.secret_key = os.urandom(32)

@app.route("/")# checks for session and sends user to appropriate spot
def checkSession():
    if 'username' in session:
        return redirect("/home")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])# will code registering and logging forms later
def login():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:# checks if both form entries were filled out
            return redirect("/login")

        #check if user has special chars

        #check for existing username
    return render_template("login.html")


#def displayHome():
   # return render_template("home.html")

@app.route("/wordle")

@app.route("/user/<int:user_id>")# viewing individual users

@app.route("/article/<int:post_id>")# viewing news posts

@app.route("/logout")
def removeSession():
    return redirect("/")

def weather_type():
    with open("keys/key_openweathermap.txt") as file:
      key = file.read().strip()
    if not key:
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
    with open("keys/key_openweathermap.txt") as file:
      key = file.read().strip()
    if not key:
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

@app.route("/home")
def NYT_api():
    with open("keys/key_NYT.txt") as file:
        key = file.read().strip()
    ##conditional for key
    rain_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=rain&api-key={key}")
    rainArticles = []
    json_d = rain_url.read()
    info = json.loads(json_d.strip())

    for i in info["response"]["docs"]:
        headline = i["headline"]["main"]
        pub_date = i["pub_date"]

        rainArticles.append({
            "headline": headline,
            "pub_date": pub_date,
        })

    snow_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=snow&api-key={key}")
    snowArticles = []
    json_d = snow_url.read()
    info = json.loads(json_d.strip())

    for i in info["response"]["docs"]:
        headline = i["headline"]["main"]
        pub_date = i["pub_date"]

        snowArticles.append({
            "headline": headline,
            "pub_date": pub_date,
        })

    sunny_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=sunny&api-key={key}")
    sunnyArticles = []
    json_d = sunny_url.read()
    info = json.loads(json_d.strip())

    for i in info["response"]["docs"]:
        headline = i["headline"]["main"]
        pub_date = i["pub_date"]

        sunnyArticles.append({
            "headline": headline,
            "pub_date": pub_date,
        })

    cloudy_url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=cloudy&api-key={key}")
    cloudyArticles = []
    json_d = cloudy_url.read()
    info = json.loads(json_d.strip())

    for i in info["response"]["docs"]:
        headline = i["headline"]["main"]
        pub_date = i["pub_date"]

        cloudyArticles.append({
            "headline": headline,
            "pub_date": pub_date,
        })

    if weather_type() == "Rain":
        main_articles = rainArticles
        weather_T = "Rainy"
    elif weather_type() == "Snow":
        main_articles = snowArticles
        weather_T = "Snowy"
    elif weather_type() == "Clear":
        main_articles = sunnyArticles
        weather_T = "Sunny"
    elif weather_type() == "Clouds":
        main_articles = cloudyArticles
        weather_T = "Cloudy"

    tmp = weather_temp()
    return render_template("home.html", main_articles=main_articles, weather_T=weather_T, tmp = tmp)


# def dict_c_api():
#     file = open("keys/key_merriam_webster_c.txt")
#     key = file.read().strip()
#     if not key:
#       print("Error: API key is missing"). 
#       return none
#     ##conditional for key
#     url = urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key={key}")
#     json_d = url.read()
#     info = json.loads(json_d.strip())
#     txt = info["meta"]["id"]
#     return render_template("home.html", txt=txt)
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
