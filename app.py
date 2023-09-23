from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorturls.db'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Url(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    longurl = db.Column('long', db.String())
    shorturl = db.Column('short', db.String(4))

    def __init__(self, long, short):
        self.longurl = long
        self.shorturl = short


@app.before_request
def create_tables():
    db.create_all()


def shortener():
    char_list = string.ascii_letters + string.digits
    while True:
        st = ''.join(random.choice(char_list) for i in range(5))
        short = Url.query.filter_by(shorturl=st).first()
        if not short:
            return st


@app.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        long_url = request.form['n']
        found_url = Url.query.filter_by(longurl=long_url).first()
        if found_url:
            return redirect(url_for("display", url=found_url.shorturl))
        else:
            short_url = shortener()
            new_url = Url(long_url, short_url)
            db.session.add(new_url)
            db.session.commit()
            found_url = Url.query.filter_by(longurl=long_url).first()
            return redirect(url_for("display", url=found_url.shorturl))
    else:
        return render_template('index.html')


@app.route('/short/<url>')
def display(url):
    return render_template("displayurl.html", display=url)


@app.route('/<short_url>')
def redirect_link(short_url):
    long_url = Url.query.filter_by(shorturl=short_url).first()
    if long_url:
        return redirect(long_url.longurl)
    else:
        return f'<h1>Url Does Not Exist</h1'


if __name__ == "__main__":
    app.run(debug=True)

