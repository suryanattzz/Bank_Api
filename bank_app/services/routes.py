from flask import (render_template,flash,redirect,url_for
                   ,request,session,Blueprint)
from bank_app.models import User,Transactions
from flask_login import current_user,login_required
from bank_app import app
from bank_app.services.forms import WithdrawForm,DepositForm
from bank_app.services.utils import sent_otp_email


services=Blueprint('services',__name__)


@services.route("/transactions",methods=['GET','POST'])
@login_required
def transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    user = Transactions.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('transactions.html',image_file=image_file,user=user)

@services.route("/withdraw",methods=['GET','POST'])
def withdraw():
    form=WithdrawForm()
    if form.validate_on_submit():
        user=User.query.filter_by(pin=form.pin.data).first()
        if user:
            session['withdrawal_amount'] = form.withdraw.data
            sent_otp_email(user)
            return redirect(url_for('verify_otp_withdraw'))
        else:
            flash('Pin Is Invalid. Please check your Four Digit Pin.','danger')
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('withdraw.html',image_file=image_file,form=form)


@services.route("/deposit",methods=['GET','POST'])
def deposit():
    form=DepositForm()
    if form.validate_on_submit():
        user=User.query.filter_by(pin=form.pin.data).first()
        if user:
            session['deposit_amount'] = form.deposit.data
            sent_otp_email(user)
            return redirect(url_for('verify_otp_deposit'))
        else:
            flash('Pin Is Invalid. Please check your Four Digit Pin.','danger')
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('deposit.html',image_file=image_file,form=form)
