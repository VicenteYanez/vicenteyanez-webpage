from flask_app import db


class Comment(db.Model):
    __tablename__ = "posts_test"

    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String(4096))
    tag = db.Column(db.String())
    time = db.Column()


db.create_all()
