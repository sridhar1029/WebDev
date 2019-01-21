from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_img, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created!!", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Unsuccessful login! Plz check the email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return  render_template('account.html', title='Account', img_file=img_file, form=form)


@users.route("/user/<string:username>", methods=['GET'])
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        q = 10
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password!", "info")
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_pw
            db.session.commit()
            flash(f"Account password has been changed!!", 'success')
            return redirect(url_for('users.login'))
        return render_template("reset_token.html", title="Reset Password", form=form)
    else:
        flash("That is an invalid or expired token!", "warning")
        return redirect(url_for("users.reset_request"))