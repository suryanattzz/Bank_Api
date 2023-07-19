from flask import (render_template,flash,redirect,
                   url_for,request,session,Blueprint)
from bank_app.models import User,Transactions
from flask_login import login_user,current_user,logout_user,login_required
from bank_app import db,bcrypt
from bank_app.users.forms import (RegistrationFrom,LoginFrom,UpdateAccountForm,
                                  RequestResetForm,ResetPasswordForm)
from bank_app.users.utils import sent_reset_email,save_picture
import random


users=Blueprint('users',__name__)


@users.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationFrom()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,
                    acc_type=form.acc_type.data,account_no=random.randint(100000, 999999),
                    aaahaar_no=form.aadhaar_number.data,image_file='default.jpg',
                pin=form.pin.data,balance=form.deposit.data,password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash(f'Account created!','success')
        login_user(user)
        trans=Transactions(account_no=current_user.account_no,balance=form.deposit.data,
                            deposit=form.deposit.data,withdraw=0.0,author=current_user)
        db.session.add(trans)
        db.session.commit()
        
        return redirect(url_for('users.account_info'))
    return render_template('register.html',title='Register',form=form) 



@users.route("/login",methods=['GET','POST'])
def login():
    form=LoginFrom()
    if form.validate_on_submit():
        user=User.query.filter_by(account_no=form.acc_no.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else :
                flash('You Have logged into your account.','success')
                return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessfull. Please check your Account Number and password','danger')
    return render_template('login.html',title='Login',form=form)

@users.route("/logout",methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/update",methods=['GET','POST'])
@login_required
def update():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
            db.session.commit()
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('acccount has been updated','success')
        return redirect(url_for('users.account_info'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('update.html',title='Update', 
                        image_file=image_file,form=form)


@users.route("/account_info",methods=['GET','POST'])
@login_required
def account_info():
    user = current_user
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account_info.html',image_file=image_file,user=user)


@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            sent_reset_email(user)
            flash('An Email Is Sent To you Email ID....','info')
            return redirect(url_for('main.home'))
    return render_template('reset_request.html',title='Reset Password',form=form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    user=User.verify_reset_token(token)
    if user is None:
        flash("Invalid or Expired Token",'warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f'Pin Has Been Updated!','success')
        return redirect(url_for('main.home'))

    return render_template('reset_token.html',title='Reset Pin',form=form)

