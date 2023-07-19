from flask_wtf import FlaskForm
from wtforms import (StringField,PasswordField,SubmitField,IntegerField)
from wtforms.validators import (DataRequired,Regexp,NumberRange)



class DepositForm(FlaskForm):
    deposit=IntegerField('Amount',
                         validators=[DataRequired(),NumberRange(min=1, message='Deposit amount must be positive')])
    pin=PasswordField('Pin',
                         validators=[DataRequired(),Regexp(r'^\d{4}$', message='Field must contain Only 4 digits.')])
    submit=SubmitField('Deposit The Amount')

class WithdrawForm(FlaskForm):
    withdraw=IntegerField('Amount',
                         validators=[DataRequired(),NumberRange(min=1, message='Withdraw amount must be positive')])
    pin=PasswordField('Pin',
                         validators=[DataRequired(),Regexp(r'^\d{4}$', message='Field must contain Only 4 digits.')])
    submit=SubmitField('Withdraw The Amount')


class OTPForm(FlaskForm):
    otp=StringField('Otp',validators=[DataRequired(),Regexp(r'^\d{4}$',
                                                            message='Field must contain Only 4 digits.')])
    submit=SubmitField('Verify OTP')

