## Quarter Collective: Ankita Saha, Evan Chan, and Jady Lei

#building so i have to touch __init__ the least amount of times possible
def createArticleCards(articles):
    output = ""
    for article in articles:
        output += '''<div class="card" style="width: 18rem;">'''
        output += '''<div class="card-body">'''
        output += f'''<a style="" href="{article[5]}"><h5>{article[1]}</h5></a>'''
        output += f'''<p><i>{article[2]}</i></p>'''
        output += f'''<p>{article[3]}</p>'''
        output += f'''<p class="hearts">Hearts: {article[4]}</p>'''
        output += f'''</div>'''
        output += f'''</div>'''
    return output

def getColors(weathercondition):
    if weathercondition == "sunny":
        background = "#b6d7a8"
        text = "#38761d"
        accent = "#fff2cc"
        accenttext = "#f6b26b"
    elif weathercondition == "cloudy":
        background = "#9fc5e8"
        text = "#ffffff"
        accent = "#6d9eeb"
        accenttext = "#ffffff"
    elif weathercondition == "rainy":
        background = "#8e7cc3"
        text = "#351c75"
        accent = "#d9d2e9"
        accenttext = "#8e7cc3"
    elif weathercondition == "snowy":
        background = "#0097a7"
        text = "#ffffff"
        accent = "#ff9900"
        accenttext = "#ffffff"
    else:
        background = "#434343"
        text = "#d9d9d9"
        accent = "#d9d9d9"
        accenttext = "#999999"
    return(background, text, accent, accenttext)

def getStyling(weatherCondition):
    colors = getColors(weatherCondition)
    output = "<style>"
    output += "body {"
    output += f"background-color: {colors[0]}"
    output += f"color: {colors[1]}"
    output += "}"
    output += ".navbar {"
    output += f"background-color: {colors[2]}"
    output += f"color: {colors[3]}"
    output += "}"
    output += "</style>"

    return output