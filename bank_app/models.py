from bank_app import db,app,login_manager
from datetime import date 
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False)
    aaahaar_no=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(120))
    pin=db.Column(db.Integer,nullable=False)
    account_no=db.Column(db.Integer,nullable=False)
    balance=db.Column(db.Integer)
    acc_type=db.Column(db.String(60),nullable=False)
    image_file=db.Column(db.String(20),nullable=False ,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Transactions',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data['user_id']
            return User.query.get(user_id)
        except:
            return None
        
    def __repr__(self):
        return f"User('{self.username}','{self.acc_type}','{self.image_file}')"
    


class Transactions(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    account_no=db.Column(db.Integer,nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=date.today)
    balance=db.Column(db.Integer)
    deposit=db.Column(db.Integer)
    withdraw=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
 






