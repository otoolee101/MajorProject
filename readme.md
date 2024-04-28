.venv\Scripts\Activate.ps1

## Install database and create admin user ##
In terminal enter the following: 
Flask shell
>>> from app.extensions import db, bcrypt
>>> from app.models.models import Cart, Assets, User, Branch, Asset_history, Order 
>>> db.create_all()
>>> admin=User(username='admin', branch_name = 'ARMYY', password=bcrypt.generate_password_hash('password').decode('utf-8'), role='admin', authorised= 'Y')
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()