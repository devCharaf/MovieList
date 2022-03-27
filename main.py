from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# create a form
class EditForm(FlaskForm):
    rating = StringField(label='Your Rating Out of 19 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


# create table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Movie {self.title}>'


# Create the database file and tables
if not os.path.isfile('movies.db'):
    db.create_all()


if not db.session.query(Movie).all():
    new_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
                    "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to "
                    "a jaw-dropping climax.",
        rating=7.3,
        ranking=10,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )

    db.session.add(new_movie)
    db.session.commit()


@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    form = EditForm()
    movie_id = request.args.get('id')
    book_selected = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
