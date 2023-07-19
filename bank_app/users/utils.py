from flask import url_for
from bank_app.models import User
from flask_mail import Message
from PIL import Image
from bank_app import app,mail
import os
import secrets


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    f_name,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex +f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def sent_reset_email(user):
    token=User.get_reset_token(user)
    msg=Message('Password Reset Request',sender='natsurya@gmail.com',
                recipients=[user.email])
    msg.body=f'''To Reset Your Password,Visit The Link:
    {url_for('users.reset_token',token=token,_external=True)}
    If You Did NOT Request This ,Then Ignore IT ......
    '''
    mail.send(msg)