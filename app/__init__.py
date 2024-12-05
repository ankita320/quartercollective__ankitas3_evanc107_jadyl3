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

@app.route("/home")
def displayHome():
    return render_template("home.html")

@app.route("/wordle")

@app.route("/user/<int:user_id>")# viewing individual users

@app.route("/article/<int:post_id>")# viewing news posts

@app.route("/logout")
def removeSession():
    return redirect("/")
# 
# def NYT_api():
#     file = open("keys/key_NYT.txt")
#     key = file.read().strip()
#     ##conditional for key
#     url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={key}")
#     json_d = url.read()
#     info = json.loads(json_d.strip())
#     txt = info["response"]["docs"]
#     return render_template("home.html", txt=txt)

# 
def dict_c_api():
    file = open("keys/key_merriam_webster_c.txt")
    key = file.read().strip()
    if not key:
      print("Error: API key is missing")
      return none
    ##conditional for key
    url = urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key={key}")
    json_d = url.read()
    info = json.loads(json_d.strip())
    txt = info["meta"]["id"]
    return render_template("home.html", txt=txt)
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
# def owm_api():
#     file = open("keys/key_openweathermap.txt")
#     key = file.read().strip()
#     if not key:
#       print("Error: API key is missing")
#       return none
#     ##conditional for key
#     city = ""
#     ##try catch/conditional if city dont exist or not spell right
#     url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?{city}&appid={key}")
#     json_d = url.read()
#     info = json.loads(json_d.strip())
# 
#     return render_template("home.html", txt=txt)

if __name__ == "__main__":
    app.debug = True
    app.run()
