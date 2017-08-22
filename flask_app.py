
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, Markup
from flask_sqlalchemy import SQLAlchemy

from content_management import Content

app = Flask(__name__)

# DB parameters
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="7candadospara7tablas",
    hostname="nasus",
    databasename="personal_website_test")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db connection
db = SQLAlchemy(app)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/projects')
def projects():
    return render_template("projects.html", projects=Content.projects_list)

@app.route('/blog/')
def blog_content(content=None):
    return render_template("content.html", menu=Content.content_dict,
                           top5=Content.top5(), content=content)


# blog posts
@app.route('/blog/weather-earthquakes/')
def weather_earthquakes():
    template = "content/weather-earthquakes/weather-earthquakes.html"
    content_file = open(template, 'r')
    content = Markup(content_file.read())
    content_file.close()
    return render_template("content.html", menu=Content.content_dict,
                           top5=Content.top5(), content=content)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", menu=Content.content_dict,
                           top5=Content.top5())


if __name__ == "__main__":
    app.run()
