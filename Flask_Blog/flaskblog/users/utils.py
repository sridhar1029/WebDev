import os
import secrets
from PIL import Image
from flask_mail import Message
from flaskblog import mail
from flask import url_for, current_app

def save_img(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img_fn = random_hex + f_ext
    img_path = os.path.join(current_app.root_path, 'static/profile_pics', img_fn)
    output_size = (125, 125)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(img_path)
    return img_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Requet', sender="noreply@demo.com", recipients=[user.email])
    msg.body = f'''
    To reset your password visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made!
    '''
    mail.send(msg)