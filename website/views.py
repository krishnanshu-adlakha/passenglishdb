from flask import Blueprint, render_template, request, redirect, session, flash
import requests
import json
from urllib.parse import unquote

views = Blueprint("views",__name__)

with open('website/json/allpoems.json') as file:
  all_poems = file.read()

all_poems = json.loads(all_poems)

with open('website/json/inspector_characters.json') as file:
  inspector_characters = file.read()

inspector_characters = json.loads(inspector_characters)

with open("website/json/rj_characters.json") as file:
    rj_characters = file.read()

rj_characters = json.loads(rj_characters)

with open("website/json/inspector.json") as file:
    inspector_quotes = file.read()

inspector_quotes = json.loads(inspector_quotes)

with open("website/json/rj.json") as file:
    rj_quotes = file.read()

rj_quotes = json.loads(rj_quotes)

with open("website/json/examples.json") as file:
    all_examples = file.read()

all_examples = json.loads(all_examples)

all_poem_names = []
for poem in all_poems:
    all_poem_names.append(poem["name"])

with open("website/json/poetry.json") as file:
    poetry_quotes = file.read()


def get_themes(quotes_list):
    themes = []

    for quote in quotes_list:
        for theme in quote["themes"]:
            if theme not in themes:
                themes.append(theme)
    
    return themes

poetry_quotes = json.loads(poetry_quotes)


@views.route("/",methods=["POST","GET"])
def home():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        quotes_data = response.json()
        quote = quotes_data[0]["q"]
        quote_author = quotes_data[0]["a"]
    except:
        quote = "Revise and you shall pass"
        quote_author = "A Wise Individual"

    return render_template("home.html",quote=quote,quote_author=quote_author)

@views.route("/bypoem/<name>")
def bypoem(name):
    name=unquote(name)
    if name == "all":
        return render_template("bypoem.html",poems=all_poems)
    elif name in all_poem_names:
        quotes = []

        for quote in poetry_quotes:
            if quote["poem"] == name:
                quotes.append({"quote":quote["quote"],"speaker":quote["poem"]})

        for quote in quotes:
            quote = quote.replace("&","/")
        return render_template("quotes.html",quotes=quotes,name=name)
    else:
        return render_template("404.html")

@views.route("/bytheme/<text>/<theme>")
def bytheme(text,theme):
    theme=unquote(theme)
    text=unquote(text)
    if theme == "all":
        if text == "poetry":
            themes = get_themes(poetry_quotes)
        elif text == "inspector":
            themes = get_themes(inspector_quotes)
        elif text == "rj":
            themes = get_themes(rj_quotes)

        return render_template("bytheme.html",themes=themes,text=text)
    
    else:
        if text == "poetry":
            all_quotes = poetry_quotes
        elif text == "inspector":
            all_quotes = inspector_quotes
        elif text == "rj":
            all_quotes = rj_quotes
        else:
            return render_template("404.html")

        quotes = []    
        for quote in all_quotes:
            if theme in quote["themes"]:
                if all_quotes == poetry_quotes:
                    quotes.append({"quote":quote["quote"],"speaker":quote["poem"]})
                else:
                    quotes.append({"quote":quote["quote"],"speaker":quote["character"]})

        for quote in quotes:
            quote.replace("&","/")
        return render_template("quotes.html",quotes=quotes,name=theme)

@views.route("bycharacter/<text>")
def bycharacter(text):
    text = unquote(text)
    if text == "inspector":
        return render_template("bycharacter.html",characters=inspector_characters)
    elif text == "rj":
        return render_template("bycharacter.html",characters=rj_characters)
    elif text in inspector_characters:
        quotes = []
        for quote in inspector_quotes:
            if text == quote["character"]:
                quotes.append({"quote":quote["quote"],"speaker":quote["character"]})
        
        return render_template("quotes.html",quotes=quotes,name=text)
    elif text in rj_characters:
        quotes = []
        for quote in rj_quotes:
            if text == quote["character"]:
                quotes.append({"quote":quote["quote"],"speaker":quote["character"]})
        
        return render_template("quotes.html",quotes=quotes,name=text)
    else:
        return render_template("404.html")

@views.route("/printquotes/<name>/<quotes>")
def printquotes(name,quotes):
    quotes_list = eval(unquote(quotes))
    name = unquote(name)
    for quote in quotes_list:
        quote = quote.replace("&","/")
    return render_template("pdf_template.html",quotes=quotes_list,name=name)

@views.route("/examples/<id>")
def examples(id):
    if id == "all":
        return render_template("examples.html", examples=all_examples)
    else:
        for example in all_examples:
            if example["id"] == id:
                return render_template("essay.html",essay=example)
            
        return render_template("404.html")

@views.route("/printessay/<id>")
def printessay(id):
    for example in all_examples:
        if example["id"] == id:
                return render_template("printessay.html",essay=example)
        
    return render_template("404.html")
                
