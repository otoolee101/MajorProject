from unittest.mock import patch
import pytest

from app.models.models import Assets 

"""Test managers can view maintain area"""
def test_view_assets_manager (client):
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_assets",follow_redirects=True)
    assert b'<td>Ship</td>' in response.data

"""Test admin can view maintain area"""
def test_view_assets_admin (client):
    client.post("/", data={"username": "admin", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_assets",follow_redirects=True)
    assert b'<td>Ship</td>' in response.data

"""Test users cannot view maintain area"""
def test_view_assets_user (client):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_assets",follow_redirects=True)
    assert b'You are not authorised to access this page' in response.data


"""Add asset as a manger"""
def test_add_asset(client):
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_asset")
 
    response = client.post("/add_asset", data={"asset_name":"Boeing 737","asset_description":"large plane","keyword":"Airplane"},follow_redirects=True)
    assert b'Asset added successfully.' in response.data

"""Add error handling on add asset"""
def test_error_add_asset(client):
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_asset")
    with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
        response = client.post("/add_asset", data={"asset_name":"Boeing 737","asset_description":"large plane","keyword":"Airplane"},follow_redirects=True)
        assert b'Asset failed to create. Please contact system administration.' in response.data
    yield
    
"""test editing an asset"""
def test_edit_asset(client, app):
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.post("/add_asset", data={"asset_name": "Boeing 737", "asset_description": "large plane", "keyword": "Airplane"}, follow_redirects=True)

    response = client.post(f"/edit_asset/{2}", data={"asset_name": "Boeing 737", "asset_description": "plane for cargo", "keyword": "Airplane", "available": "True"}, follow_redirects=True)
    
    assert b'Asset updated successfully' in response.data
    
    with app.app_context():
            asset =Assets.query.filter_by(asset_name='Boeing 737',asset_description='plane for cargo').first()
            assert asset is not None

"""Test error handling for edit asset"""
def test_error_edit_asset(client):
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_assets")
    with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
        response = client.post(f"/edit_asset/{1}", data={"asset_name": "Ship", "asset_description": "plane for cargo", "keyword": "Airplane", "available": "Y"}, follow_redirects=True)
    
        assert b'Asset failed to update' in response.data
    yield

"""Testing delete asset"""    
def test_delete_asset(client,app): 
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_assets")
    response = client.post("/delete_asset/",data= {"asset_id":"1"},  follow_redirects=True)
    assert b'Asset was deleted successfully.' in response.data

    with app.app_context():
        asset =Assets.query.filter_by(asset_name='Ship').first()
        assert asset is None
    
"""Testing error handling for delete asset """
def test_error_delete_asset(client,app): 
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_assets")
    with patch('app.models.models.db.session.commit', side_effect=Exception("Database commit failed")):
        response = client.post("/delete_asset/",data= {"asset_id":"1"},  follow_redirects=True)
        assert b'Asset failed to delete.' in response.data
    yield

#maintain user