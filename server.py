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

    

    return render_template("user_detail.html")

@app.route('/login', methods=['GET'])
def login():
    """User login screen."""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_or_create_new():
    """User log ins or create new if username not in database."""

    email = request.form.get("user_email")
    password = request.form.get("password")

    dbuser = User.query.filter(User.email == email).first()

    if dbuser:
        if dbuser.password == password:
            flash("Logged in")
            session["logged_in_useremail"] = email
            return redirect("/")
        else: 
            flash("Wrong Password")
            return redirect("/login")
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("You are added.")
        session["logged_in_useremail"] = email
        return redirect('/')


@app.route('/logout')
def logout():
    """User successfully loged out."""

    print session.keys()
    session.pop("logged_in_useremail", None)
    print session.keys()
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
