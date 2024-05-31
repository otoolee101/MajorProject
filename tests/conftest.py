import os
from flask import config
import pytest

from app.__init__ import create_app
from app.extensions import db, bcrypt
from app.models.models import User, Branch, Assets
from config import *
 
@pytest.fixture()
def app():
    os.environ["PROD_APP_SETTINGS"] = "config.TestConfig"
    app=create_app()
    ctx=app.app_context()
    ctx.push()

    with ctx:
        db.create_all()
        user=User(username='testuser', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/'), role='user', authorised = 'Y', failed_login_attempts = 0)
        db.session.add(user)
        admin=User(username='admin', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/'), role='admin', authorised = 'Y', failed_login_attempts = 0)
        db.session.add(admin)
        manager=User(username='manager', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/'), role='manager', authorised = 'Y', failed_login_attempts = 0)
        db.session.add(manager)
        branch=Branch(branch_name = 'Navy', address_line1 ='Liverpool Street', postcode = 'L1 6PN')
        branch2=Branch(branch_name = 'Army', address_line1 ='St Johns Street', postcode = 'L1 6PN')
        db.session.add(branch,branch2)
        asset=Assets(asset_name= 'Ship', asset_description='Queen Elizabeth Ship', keyword = 'Ship', available = 'Y')
        db.session.add(asset)
        db.session.commit()
        

    yield app
    db.drop_all()
    
@pytest.fixture()
def client(app):
    return app.test_client()
