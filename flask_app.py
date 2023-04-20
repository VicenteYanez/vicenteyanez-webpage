
# A very simple Flask Hello World app for you to get started with...

import os
from flask import Flask, render_template, Markup, send_file
from content_management import Content

import numpy as np

app = Flask(__name__)

listcontent = Content()
filepath = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def homepage(content=None):
    return render_template("index.html", posts=listcontent.lists(), maps=listcontent.maps())


@app.route('/aboutme/')
def aboutme():
    return render_template("aboutme.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route('/images/backgroundandes')
def andes_background():
    background = "{}/static/images/background-bw.jpg".format(filepath)
    return send_file(background)


# posts
@app.route('/<content>/<post_name>')
def show_post(content, post_name):
    # posts
    if content == "content":
        template = "{}/content/{}/{}.html".format(filepath, post_name, post_name)
    elif content == "maps":
        template = "{}/content/portfolio/{}.html".format(filepath, post_name, post_name)

    # table = np.loadtxt('content/weather-earthquakes/code/corr_coef.txt', fmt='%s', delimiter=';')
    content_file = open(template, 'r')
    content = Markup(content_file.read())
    content_file.close()
    
    return render_template("content.html", content=content)


if __name__ == "__main__":
    #app.debug = True 
    app.run()
