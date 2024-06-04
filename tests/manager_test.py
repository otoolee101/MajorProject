from unittest.mock import patch
import pytest
from app.extensions import db
from app.models.models import Assets, Order

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


"""Test asset as a manger"""
def test_add_asset(client):
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_asset")
 
    response = client.post("/add_asset", data={"asset_name":"Boeing 737","asset_description":"large plane","keyword":"Airplane"},follow_redirects=True)
    assert b'Asset added successfully.' in response.data

"""Test error handling on add asset"""
def test_add_asset_exception(client, app, monkeypatch):
    def mock_add_asset(*args, **kwargs):
        raise Exception("Database add operation failed")
    
    monkeypatch.setattr(db.session, 'add', mock_add_asset)
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    client.get("/maintain_asset")
    response = client.post("/add_asset", data={"asset_name":"Boeing 737","asset_description":"large plane","keyword":"Airplane"},follow_redirects=True)
    assert b'Asset failed to create. Please contact system administration.' in response.data
    
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
def test_edit_asset_exceptionn(client, monkeypatch):
    def mock_commit(*args, **kwargs):
        raise Exception("Database commit failed")
    response= client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    assert b"AssetHub" in response.data
    client.get("/maintain_assets",follow_redirects=True)
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    response = client.post(f"/edit_asset/{1}", data={"asset_name": "Ship", "asset_description": "plane for cargo", "keyword": "Airplane", "available": "Y"}, follow_redirects=True)
    assert b"Asset failed to update" in response.data

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
def test_delete_asset_exceptionnn(client, app):
    def mock_delete(*args, **kwargs):
        raise Exception("Database delete failed")

    with patch('app.manager.routes.db.session.delete', mock_delete):
        client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
        # Assume asset_id is obtained from the database or another route
        response = client.post("/delete_asset/", data={"asset_id": 1}, follow_redirects=True)
        assert b"Asset failed to delete." in response.data


"""Testing viewing asset history""" 
def test_asset_history(client): 
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post ("/checkout", follow_redirects=True)

    response = client.get(f"/asset_history/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    assert b'manager' in response.data
    assert b'Order Placed' in response.data

"""Test error handling for viewing asset history"""
def test_error_asset_history(client, monkeypatch):
    def mock_query_filter_by(*args, **kwargs):
        raise Exception("Database query failed")
    monkeypatch.setattr(Order, 'query', type('FakeQuery', (), {'filter_by': mock_query_filter_by}))
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/asset_history/1")
    assert b"An error occurred retrieving assets." in response.data

"""Test viewing orders as a manager"""
def test_viewing_orders(client): 
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post ("/checkout", follow_redirects=True)
    
    response = client.get("/maintain_orders/",follow_redirects=True)
    assert b'<td>Ship</td>' in response.data

"""Test editing an order as a manager"""
def test_editing_orders(client, app): 
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post ("/checkout", follow_redirects=True)
   
    response= client.post(f"/edit_order/{asset.asset_id}", data={"asset_id": asset.asset_id, "status":"Order Shipped"}, follow_redirects=True)
    assert b'Order updated successfully' in response.data
    
    with app.app_context():
            order=Order.query.filter_by(asset_id='1', status = 'Order Shipped').first()
            assert order is not None

"""Test error handling of editing an order as a manager"""
def test_edit_order_exception(client, monkeypatch):
    def mock_commit(*args, **kwargs):
        raise Exception("Database commit failed")
    response= client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    assert b"AssetHub" in response.data
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post ("/checkout", follow_redirects=True)
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    response= client.post(f"/edit_order/{asset.asset_id}", data={"asset_id": asset.asset_id, "status":"Order Shipped"}, follow_redirects=True)

    assert b"An error occurred while updating order status" in response.data

"""Test error handling for viewing all assets"""
def test_error_viewing_assets(client, monkeypatch):
    def mock_query_filter_by(*args, **kwargs):
        raise Exception("Database query failed")
    monkeypatch.setattr(Assets, 'query', type('FakeQuery', (), {'filter_by': mock_query_filter_by}))
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_assets",follow_redirects=True )
    assert b"An error occurred retrieving assets." in response.data

"""Test error handing for viewing all orders"""
def test_error_viewing_orders(client, monkeypatch):
    def mock_query_filter_by(*args, **kwargs):
        raise Exception("Database query failed")
    monkeypatch.setattr(Order, 'query', type('FakeQuery', (), {'filter_by': mock_query_filter_by}))
    client.post("/", data={"username": "manager", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/maintain_orders",follow_redirects=True )
    assert b"An error occurred retrieving orders." in response.data

