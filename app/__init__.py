from flask import Flask, render_template
import json
import urllib.request

app = Flask(__name__)


@app.route("/")


def NYT_api():
   file = open("keys/key_NYT.txt")
   key = file.read().strip()
   url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={key}")
   json_d = url.read()
   info = json.loads(json_d.strip())
   

def NYT_api():
   file = open("keys/key_NYT.txt")
   key = file.read().strip()
   url = urllib.request.urlopen(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={key}")
   json_d = url.read()
   info = json.loads(json_d.strip())
   
   

if __name__ == "__main__":
    app.debug = True
    app.run()