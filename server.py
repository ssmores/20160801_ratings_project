"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Show user information."""

    user_details = User.query.filter(User.user_id == user_id).one()
    user_age = user_details.age
    user_zip = user_details.zipcode

    complete_user_ratings = user_details.ratings
    print complete_user_ratings

    return render_template("user_detail.html", 
                           user_id=user_id, 
                           age=user_age, 
                           zipcode=user_zip,
                           ratings=complete_user_ratings)


@app.route('/movies')
def show_movies():
    """Show all movies."""

    movies = Movie.query.order_by('title').all()

    return render_template("movies_list.html", 
                            movies=movies)


@app.route('/movies_list/<movie_id>')
def movie_details(movie_id):
    """Show movie details."""

    # Getting movie object filtered on the movie_ID passed into function.
    movie_detail = Movie.query.filter(Movie.movie_id == movie_id).one()
    title = movie_detail.title
    release_date = movie_detail.release_at
    url = movie_detail.imdb_url

    ratings = movie_detail.ratings
    

    return render_template("movie_detail.html", 
                           movie=movie_detail, 
                           title=title,
                           release_date=release_date,
                           url=url,
                           ratings=ratings)


@app.route('/login', methods=['GET'])
def login():
    """User login screen."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_or_create_new():
    """User log ins or create new if username not in database."""

    email = request.form.get("user_email")
    password = request.form.get("password")

    # Query the users table in database for user provided email.
    dbuser = User.query.filter(User.email == email).first()

    if dbuser:
        if dbuser.password == password:
            flash("Logged in")
            session["logged_in_useremail"] = email
            user_url_id = str(dbuser.user_id)
            return redirect("/users/" + user_url_id)
        else: 
            flash("Wrong Password")
            return redirect("/login")
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("You are added.")
        session["logged_in_useremail"] = email
        user_url_id = str(user.user_id)
        return redirect('/users/' + user_url_id)


@app.route('/logout')
def logout():
    """User successfully loged out."""

    session.pop("logged_in_useremail", None)
    flash("You are now logged out.")
    return redirect('/')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
