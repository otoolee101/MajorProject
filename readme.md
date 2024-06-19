# Installation Instructions #
## Create a virutal environment ## 
- Open "Ellie_OToole_Assignment" folder structure in VSCode. 
- View>Command Palette
- Select "Python : Create Environment"
- Select "Venv"
- Select Python Version 
- Tick requirements.txt
- enter into command .venv\Scripts\Activate.ps1

## Install database and create admin user ##
In terminal enter the following: 
Flask shell
>>> from app.extensions import db, bcrypt
>>> from app.models.models import Cart, Assets, User, Branch, Order 
>>> db.create_all()
>>> branch= Branch(branch_name = 'Head Office', address_line1 = 'Norcorss Road', address_line2 = 'Blackpool', postcode ='FY3 1TL')
>>> admin=User(username='admin', branch_id = 1, password=bcrypt.generate_password_hash('Assignment1/').decode('utf-8'), role='admin', authorised= 'Y')
>>> db.session.add(admin,branch)
>>> db.session.commit()
>>> exit() 

## Run application ##
In terminal enter the following: 
flask run

To access admin login with the following credentials:
username: admin
password: Assignment1/

To access manager login in with the following: 
username: manager
password: Assignment1/

To access manager user in with the following: 
username: user
password: Assignment1/

## Testing ##
To complete test run the following into the terminal: 
coverage run -m pytest

To see coverage report run the following into the terminal: 
coverage report -m

