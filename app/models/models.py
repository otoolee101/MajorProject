from app.extensions import db
from flask_login import UserMixin

#Create table to store user accounts 
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    branch_name = db.Column(db.String(9), nullable=False, unique=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(5), nullable=False, default='user')
    authorised =db.Column(db.String(1), nullable=False, default='N')
    failed_login_attempts = db.Column(db.Integer,nullable=False, default=0)
     
    def get_id(self):
        return str(self.user_id)

#Create table to store branch details 
class branch(db.Model):
    __tablename__ = 'branch'
    branch_id = db.Column(db.Integer, primary_key=True, nullable=False)
    branch_name = db.Column(db.String(50), nullable=False)
    address_line1 = db.Column(db.String(225), nullable=False)
    address_line2 = db.Column(db.String(225), nullable=False)
    postcode = db.Column(db.String(8), nullable=False) 

#Create table to store products 
class assets(db.Model):
    __tablename__ = 'assets'
    asset_id = db.Column(db.Integer, primary_key=True, nullable=False)
    asset_name = db.Column(db.String(100), nullable=True)
    asset_description = db.Column(db.String(225), nullable=True)
    keyword = db.Column(db.String(50), nullable=False)
    available =  db.Column(db.String(50), nullable=False, default = 'Y')

#Create table to record actions on each asset
class asset_history(db.Model):
    __tablename__ = 'asset_history'
    asset_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    check_out_date = db.Column(db.Date,nullable=False)
    return_date = db.Column(db.Date,nullable=False)

#Create table to store cart infromation 
class cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    assset_name = db.Column(db.String(100), nullable=False)
    branch_name = db.Column(db.String(50), nullable=False)


#Create table to store order
class order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    assset_name = db.Column(db.String(100), nullable=False)
    branch_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date,nullable=False)