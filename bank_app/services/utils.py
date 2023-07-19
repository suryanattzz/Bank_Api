from flask import render_template,flash,redirect,url_for,session
from bank_app.models import User,Transactions
from flask_login import current_user
from flask_mail import Message
from bank_app import app,db,mail
from bank_app.services.forms import OTPForm
import random


MAX_OTP_TRIES = 3
@app.route("/verify_otp_withdraw", methods=['GET', 'POST'])
def verify_otp_withdraw():
    form = OTPForm()
    otp_tries = session.get('otp_tries', 0)
    if otp_tries >= MAX_OTP_TRIES:
        flash('Maximum OTP verification tries exceeded. Please try again later.', 'danger')
        session['otp_tries'] = 0
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        otp = (form.otp.data)
        if str(otp) == str(session.get('otp')):
            withdrawal_amount = session.get('withdrawal_amount')
            current_user.balance = int(current_user.balance) - withdrawal_amount
            db.session.commit()

            trans = Transactions(account_no=current_user.account_no, balance=current_user.balance,
                                deposit=0.0, withdraw=withdrawal_amount, author=current_user)
            db.session.add(trans)
            db.session.commit()
            session['otp_tries'] = 0
            flash('Amount has been withdrawn from the account!', 'success')
            return redirect(url_for('users.account_info'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            session['otp_tries'] = otp_tries + 1
    return render_template('verify_otp.html', form=form)

def sent_otp_email(user):
    otp=random.randint(1000, 9999)
    session['otp'] = (otp)
    msg=Message('Otp For Transaction',sender='natsurya@gmail.com',
                recipients=[user.email])
    msg.body=f'''Here It Is Your Four Digit Otp For Your Transaction:
    {otp}
    If You Did NOT Request This ,Then Ignore IT ......
    '''
    mail.send(msg)


@app.route("/verify_otp_deposit", methods=['GET', 'POST'])
def verify_otp_deposit():
    form = OTPForm()
    otp_tries = session.get('otp_tries', 0)

    if otp_tries >= MAX_OTP_TRIES:
        flash('Maximum OTP verification tries exceeded. Please try again later.', 'danger')
        session['otp_tries'] = 0
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        otp = (form.otp.data)
        if str(otp) == str(session.get('otp')):
            deposit_amount = session.get('deposit_amount')
            current_user.balance = int(current_user.balance) + deposit_amount
            db.session.commit()
            trans = Transactions(account_no=current_user.account_no, balance=current_user.balance,
                                deposit=deposit_amount, withdraw=0.0, author=current_user)
            db.session.add(trans)
            db.session.commit()
            session['otp_tries'] = 0
            flash('Amount has been deposited from the account!', 'success')
            return redirect(url_for('users.account_info'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            session['otp_tries'] = otp_tries + 1
    return render_template('verify_otp.html', form=form)