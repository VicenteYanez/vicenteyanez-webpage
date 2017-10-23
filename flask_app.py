
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, Markup
from content_management import Content

import numpy as np

app = Flask(__name__)

listcontent = Content()


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/projects/')
def projects():
    return render_template("projects.html", projects=listcontent.projects_list)


@app.route('/blog/')
@app.route('/blog/categories/<category>')
def blog_content(content=None, category='None'):
    return render_template("content.html", menu=listcontent.content_dict,
                           top5=listcontent.top5(), content=content,
                           category=category)


@app.route('/aboutme/')
def aboutme():
    return render_template("aboutme.html")


@app.route('/data/')
def data():
    return render_template("data.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", menu=listcontent.content_dict,
                           top5=listcontent.top5())


# blog posts
@app.route('/blog/building-the-blog-1/')
def weather_earthquakes(category='empty'):
    template = "content/weather-earthquakes/weather-earthquakes.html"
    # table = np.loadtxt('content/weather-earthquakes/code/corr_coef.txt', fmt='%s', delimiter=';')
    content_file = open(template, 'r')
    content = Markup(content_file.read())
    content_file.close()
    return render_template("content.html", menu=listcontent.content_dict,
                           top5=listcontent.top5(), content=content,
                           category=category)


if __name__ == "__main__":
    app.run()
