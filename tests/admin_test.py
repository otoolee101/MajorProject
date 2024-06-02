from unittest.mock import patch
import pytest
from app.models.models import User, Branch

"""Test admin page cannot be accessed by a normal user"""
def test_normal_user_cannot_access_admin(client): 
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_user",follow_redirects=True)
    assert b'You are not authorised to access this page' in response.data

"""Test admin page can be accessed by admin"""
def test_admin_can_access_maintain_user(client): 
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_user",follow_redirects=True)
    assert b'Admin' in response.data

"""Test altering role"""
def test_change_user_role(client, app):
    client.post('/', data={"username": "admin", "password": "Assignment1/"}, follow_redirects = True)
    client.get("/maintain_user") 
    client.get('/edit_user/1')

    response = client.post('/edit_user/1', data={"username":"testuser","branch_name":"1","role": "admin","authorised":"Y"}, follow_redirects = True)
    assert b'User updated successfully'in response.data
    with app.app_context():
        user =User.query.filter_by(username='testuser',role='admin').first()
        assert user is not None

"""Test a user cannot alter a role"""
def test_change_user_role_as_user(client, app):
    client.post('/', data={"username": "testuser", "password": "Assignment1/"}, follow_redirects = True)

    response = client.get('/edit_user/1', follow_redirects = True)
    assert b'You are not authorised to access this page'in response.data
    

"""Test expection handling when editing user"""
def test_error_editing_user(client):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_user")
    response = client.get("/edit_user/1")
    with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
        response = client.post("/edit_user/1", data={"username":'admin',"branch_name": "2", "role":'admin',"authorised":"Y"},follow_redirects=True)
        assert b"User failed to update" in response.data  
    
"""Test changing account to authorised"""
def test_authorise_user(client, app):
    client.post("/register/", data={"username": "testuser1", "branch_name": "1", "password": "Assignment1/"}, follow_redirects=True)
    client.post('/', data={"username": "testuser1", "password": "Assignment1/"}, follow_redirects = True)  
    client.post('/', data={"username": "admin", "password": "Assignment1/"}, follow_redirects = True)
    client.get("/maintain_account") 

    response = client.post('/edit_user/4', data={"username":"testuser1","branch_name":"1","role": "user","authorised":"Y"}, follow_redirects = True)
    assert b'User updated successfully'in response.data
        
    with app.app_context():
        user =User.query.filter_by(username='testuser1',authorised='Y').first()
        assert user is not None

"""Test changing account to unauthorised"""
def test_unauthorise_user(client, app):
    response= client.post('/', data={"username": "testuser", "password": "Assignment1/"}, follow_redirects = True)
    assert b'AssetHub'in response.data
    
    client.post('/', data={"username": "admin", "password": "Assignment1/"}, follow_redirects = True)
    client.get("/manage_user") 
    response = client.post('/edit_user/1', data={"username":"testuser","branch_name":"1","role": "admin","authorised":"N"}, follow_redirects = True)
    assert b'User updated successfully'in response.data
    
    response= client.post('/', data={"username": "testuser1", "password": "Assignment1/"}, follow_redirects = True)
    assert b'Unsucessful sign in. Either username/password incorrect, account locked or unauthorised.' in response.data
    
    with app.app_context():
        user =User.query.filter_by(username='testuser',authorised='N').first()
        assert user is not None

"""Test deleting a user"""
def test_delete_user(client,app): 
    client.post('/', data={"username": "admin", "password": "Assignment1/"}, follow_redirects = True)
    response= client.post('/delete_user/', data= {"id":"1"}, follow_redirects=True)
    assert b'User was deleted successfully.' in response.data
    with app.app_context():
        user =User.query.filter_by(username='testuser').first()
        assert user is None

"""Test expection handling when deleting user"""
def test_error_deleting_user(client):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    
    with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
        response = client.post('/delete_user/', data= {"id":"1"}, follow_redirects=True)
        assert b'User failed to delete' in response.data

"""Test deleting a user by another user doesnt work"""
def test_delete_user_by_user(client,app): 
    client.post('/', data={"username": "testuser", "password": "Assignment1/"}, follow_redirects = True)
    response= client.post('/delete_user/', data= {"id":"2"}, follow_redirects=True)
    assert b'You are not authorised to access this page' in response.data
    with app.app_context():
        user =User.query.filter_by(username='admin').first()
        assert user is not None

"""Test branch infomation returns when selecting maintain branch"""
def test_retrieving_branch(client):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_branch",follow_redirects=True)
    assert b'<td>Navy</td>' in response.data

"""Test adding a new branch"""
def test_add_branch(client, app):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    response = client.post("/add_branch",data={"branch_name": "Air Force", "address_line1": "Walker House", "postcode": "L3 4PQ"}, follow_redirects=True)
    assert b'Branch added successfully.' in response.data

    with app.app_context():
        branch =Branch.query.filter_by(branch_name='Air Force').first()
        assert branch is not None
        
"""Testing exception handling for add branch"""
def test_error_add_branch(client):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_branch")
    with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
        response = client.post("/add_branch",data={"branch_name": "Air Force", "address_line1": "Walker House","address_line1":"Liverpool", "postcode": "L3 4PQ"}, follow_redirects=True)
        assert b"Branch failed to create." in response.data
        yield

"""Test editing branch detail and ensuring old brach name is no longer in the tables."""
def test_edit_branch(client, app):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_branch")
    response = client.get("/edit_branch/1")
    assert b'Edit Branch' in response.data
    response = client.post('/edit_branch/1', data={"branch_name":"Air","address_line1":"Walkers", "address_line2":"no", "postcode":"L2"}, follow_redirects = True)
    assert b'Branch updated successfully'in response.data

    with app.app_context():
        branch =Branch.query.filter_by(branch_name='Air').first()
        assert branch is not None

    with app.app_context():
        branch =Branch.query.filter_by(branch_name='Navy').first()
        assert branch is None

"""Test deleting newly created branch"""
def test_delete_branch(client, app):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    client.post("/add_branch", data={"branch_name": "Air Force", "address_line1": "Walker House", "postcode": "L3 4PQ"}, follow_redirects=True)

    with app.app_context():
        new_branch = Branch.query.filter_by(branch_name="Air Force").first()
        assert new_branch is not None 

    response = client.post("/delete_branch/", data={"branch_id": new_branch.branch_id}, follow_redirects=True)
    assert b'Branch was deleted successfully.' in response.data

"""Test error handling on deleting branch"""
def test_error_delete_branch(client,app):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    client.post("/add_branch", data={"branch_name": "Air Force", "address_line1": "Walker House", "postcode": "L3 4PQ"}, follow_redirects=True)

    with app.app_context():
        new_branch = Branch.query.filter_by(branch_name="Air Force").first()
        assert new_branch is not None 
        with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
            response = client.post("/delete_branch/", data={"branch_id": new_branch.branch_id}, follow_redirects=True)
            assert b'Branch failed to delete.' in response.data

"""logging messages
def test_logging_messages(client): 
    response= client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    print(response.data)
    assert b'Username: admin logged in successfully' in response.data
"""