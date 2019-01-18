from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app

posts = [
    {
        "author": "Sridhar",
        "title": "Blog Post 1",
        "content": "Some random text for bp 1",
        "date_posted": "April 25, 2018"
    },
    {
        "author": "Sneha",
        "title": "Blog Post 2",
        "content": "Some random text for bp 2",
        "date_posted": "August 9, 2018"
    },
    {
        "author": "Lobo",
        "title": "Blog Post 3",
        "content": "Some random text for bp 3",
        "date_posted": "Dec 31, 2018"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'sdng123@gmail.com' and form.password.data == 'qwerty':
            flash('Welcome Sridhar Adhikarla B-)', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful login! Plz check the email or password', 'danger')
    return render_template('login.html', title='Login', form=form)