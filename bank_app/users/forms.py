from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed

from wtforms import (StringField,PasswordField,SubmitField,
    BooleanField,SelectField,IntegerField)
from wtforms.validators import (DataRequired,Length,Email,
                                EqualTo,ValidationError,Regexp,NumberRange)
from bank_app.models import User


class LoginFrom(FlaskForm):
    acc_no=IntegerField('Account Number',
                         validators=[DataRequired()])

    password= PasswordField('Password',validators=[DataRequired()])

    remember=BooleanField('Remember Me')

    submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username=StringField('Username',
                        validators=[DataRequired(),Length(min=2 ,max=20)])

    email=StringField('Email',validators=[DataRequired(),Email()])
    picture =FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')


class RegistrationFrom(FlaskForm):
    username=StringField('Username',
                         validators=[DataRequired(),Length(min=2 ,max=20)])
    
    email=StringField('Email',validators=[DataRequired(),Email()])

    aadhaar_number=StringField('Aadhaar Number',
                               validators=[DataRequired(),Regexp(r'^\d{16}$', message='Field must contain 16 digits.')])
    password= PasswordField('Password',
                            validators=[DataRequired()])
    
    acc_type = SelectField('Account Type', 
                           validators=[DataRequired()],choices=[('','Please Select Account Type'),('Savings', 'Savings'), ('Current', 'Current') ])
    deposit=IntegerField('Deposit Amount',
                         validators=[DataRequired(),NumberRange(min=300, message='Deposit amount must be minimum of 300.')])
    pin=StringField('Pin',
                         validators=[DataRequired(),Regexp(r'^\d{4}$', message='Field must contain Only 4 digits.')])
    confirm_password= PasswordField('Confirm Password',
                                   validators=[DataRequired(),EqualTo('password')])
 
    submit=SubmitField('Sign Up')

    def validate_aadhaar(self,aadhaar_no):
        user=User.query.filter_by(aadhaar_no=aadhaar_no.data).first()
        if user is None:
            raise ValidationError("There Is Already Account With The Aadhaar Number,Try Again.")


class RequestResetForm(FlaskForm):
   
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request Password Reset')
    def validate_email(self,email):
       
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("NO Account With The Email,Check your Email ID.")


class ResetPasswordForm(FlaskForm):
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',
                                   validators=[DataRequired(),EqualTo('password')])

    submit=SubmitField('Reset Password')