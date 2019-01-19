import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created!!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful login! Plz check the email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_img(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img_fn = random_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/profile_pics', img_fn)
    output_size = (125, 125)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(img_path)
    return img_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            img_fn = save_img(form.picture.data)
            current_user.image_file = img_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You details have been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return  render_template('account.html', title='Account', img_file=img_file, form=form)

