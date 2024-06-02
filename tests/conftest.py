import pytest
import os
from app import create_app
from app.extensions import db, bcrypt
from app.models.models import User, Branch, Assets, Order
from config import TestConfig

@pytest.fixture(scope='function')
def app():
    os.environ["PROD_APP_SETTINGS"] = "config.TestConfig"
    app = create_app()
    app.config.from_object(TestConfig)
    ctx = app.app_context()
    ctx.push()

    with ctx:
        db.create_all()
        # Add initial data to the database
        user = User(username='testuser', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='user', authorised='Y', failed_login_attempts=0)
        db.session.add(user)
        admin = User(username='admin', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='admin', authorised='Y', failed_login_attempts=0)
        db.session.add(admin)
        manager = User(username='manager', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='manager', authorised='Y', failed_login_attempts=0)
        db.session.add(manager)
        branch = Branch(branch_name='Navy', address_line1='Liverpool Street', postcode='L1 6PN')
        branch2 = Branch(branch_name='Army', address_line1='St Johns Street', postcode='L1 6PN')
        db.session.add(branch)
        db.session.add(branch2)
        asset = Assets(asset_name='Ship', asset_description='Queen Elizabeth Ship', keyword='Ship', available='Y')
        db.session.add(asset)
        db.session.commit()

    yield app

    # Cleanup
    db.session.remove()
    db.drop_all()
    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        # Add initial data to the database
        user = User(username='testuser', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='user', authorised='Y', failed_login_attempts=0)
        db.session.add(user)
        admin = User(username='admin', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='admin', authorised='Y', failed_login_attempts=0)
        db.session.add(admin)
        manager = User(username='manager', branch_id=1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='manager', authorised='Y', failed_login_attempts=0)
        db.session.add(manager)
        branch = Branch(branch_name='Navy', address_line1='Liverpool Street', postcode='L1 6PN')
        branch2 = Branch(branch_name='Army', address_line1='St Johns Street', postcode='L1 6PN')
        db.session.add(branch)
        db.session.add(branch2)
        asset = Assets(asset_name='Ship', asset_description='Queen Elizabeth Ship', keyword='Ship', available='Y')
        db.session.add(asset)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()
