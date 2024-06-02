.venv\Scripts\Activate.ps1

## Install database and create admin user ##
In terminal enter the following: 
Flask shell
>>> from app.extensions import db, bcrypt
>>> from app.models.models import Cart, Assets, User, Branch, Asset_history, Order 
>>> db.create_all()
>>> branch= Branch(branch_name = 'Head Office', address_line1 = 'Norcorss Road', address_line2 = 'Blackpool', postcode ='FY3 1TL')
>>> admin=User(username='admin', branch_id = 1, password=bcrypt.generate_password_hash('password').decode('utf-8'), role='admin', authorised= 'Y')
>>> db.session.add(admin,branch)
>>> db.session.commit()
>>> exit() 
test git actions ..