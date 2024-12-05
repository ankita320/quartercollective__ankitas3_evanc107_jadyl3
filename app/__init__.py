from flask import Flask, render_template
import json
import urllib.request

app = Flask(__name__)


@app.route("/")


def NYT_api():
   file = open("keys/key_NYT.txt")
   key = file.read().strip()
    ##conditional for key
   url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={key}")
   json_d = url.read()
   info = json.loads(json_d.strip())
   

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

def dict_e_api():
   file = open("keys/key_merriam_webster_e.txt")
   key = file.read().strip()
   if not key:
      print("Error: API key is missing")
      return none
    ##conditional for key
   url = urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/sd2/json/school?key={key}")
   json_d = url.read()
   info = json.loads(json_d.strip())

##function that returns user's input for city

def owm_api():
   file = open("keys/key_openweathermap.txt")
   key = file.read().strip()
   if not key:
      print("Error: API key is missing")
      return none
   ##conditional for key
   city = ""
   ##try catch/conditional if city dont exist or not spell right
   url = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?{city}&appid={key}")
   json_d = url.read()
   info = json.loads(json_d.strip())
   
   

if __name__ == "__main__":
    app.debug = True
    app.run()