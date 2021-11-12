from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
# import pymysql
from datetime import datetime
import sqlite3
from sqlalchemy import Column, Integer, String, Text, Date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%s@localhost/mydb" % quote('password')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Blogs(db.Model):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    author = Column(String(200))
    desc = Column(Text(200), nullable=True)
    date_created = Column(Date)
    img = Column(String(200))


@app.route('/')
def index():
    print('hi')
    blogs = db.session.query(Blogs).all()

    return render_template("index.html", blogs=blogs)


@app.route('/add/')
def add():
    return render_template("add.html")


@app.route('/addblog/', methods=['POST'])
def addtask():
    title = request.form['title']
    author = request.form['author']
    desc = request.form['desc']

    task = Blogs(title=title, author=author, desc=desc, date_created=datetime.now())

    db.session.add(task)

    # blogs = db.session.query(Blogs).all()
    # count = list(blogs)
    # id=len(count)
    # blog = db.session.query(Blogs).filter(Blogs.id==id)
    # if id < 6:
    #     blog.img="../static/img/img"+blog.id+".jpg"
    # else :
    #     blog.img="../static/img/no-image.jpg"

    db.session.commit()
    return redirect('/')


@app.route('/read/<int:id>/')
def read(id):
    blogs = db.session.query(Blogs).filter(Blogs.id == id)
    return render_template("read_blog.html", blogs=blogs)


@app.route('/delete/<int:id>/')
def delete(id):
    task = db.session.query(Blogs).filter(Blogs.id == id)
    task.delete()
    db.session.commit()
    return redirect('/')


@app.route('/search/', methods=['POST'])
def search():
    title = request.form['searched']
    selected_blog = db.session.query(Blogs).filter(Blogs.title == title)
    if selected_blog.count() == 0:
        return render_template("noblog.html")
    return render_template("read_blog.html", blogs=selected_blog)


if __name__ == "__main__":
    try:
        db.create_all()
    except:
        pass
    app.run(debug=True)  # ,host="127.0.0.1", port=5000
