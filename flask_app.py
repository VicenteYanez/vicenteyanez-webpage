
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from content_management import Content

app = Flask(__name__)

# DB parameters
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="vicenteyanez",
    password="7candadospara7tablas",
    hostname="vicenteyanez.mysql.pythonanywhere-services.com",
    databasename="vicenteyanez$personal-website-test")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db connection
db = SQLAlchemy(app)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/blog/')
def content():
    return render_template("content.html", menu=Content.content_dict,
                           top5=Content.top5())


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", menu=Content.content_dict,
                           top5=Content.top5())


if __name__ == "__main__":
    app.run()
