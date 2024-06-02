from unittest.mock import patch
from flask import url_for
import pytest
from app.models.models import Assets, Cart,Order
from app.extensions import db


"""Test home page loads"""
def test_home_page(client): 
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/home", follow_redirects =True)
    assert b'AssetHub' in response.data

"""Test borrow asset page returns all assets"""
def test_borrow_asset(client):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/borrow_asset", follow_redirects =True)
    assert b'<td>Ship</td>' in response.data

"""Test error handling of borrowing assets"""
def test_error_borrow_asset(client, monkeypatch):
    class FakeAssetsQuery:
        @staticmethod
        def filter(*args, **kwargs):
            raise Exception("Database query failed")
    monkeypatch.setattr(Assets, 'query', FakeAssetsQuery)
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get("/borrow_asset", follow_redirects=True)
    assert b"An error occurred retrieving assets." in response.data

"""Test adding an item to the cart and checking it becomes unavailable in shop"""
def test_add_to_cart(client, app):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    response = client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    assert b'Item added successfully.' in response.data

    with app.app_context():
            cart=Cart.query.filter_by(asset_id='1').first()
            assert cart is not None
    
    with app.app_context():
            asset=Assets.query.filter_by(asset_id='1', available='N').first()
            assert asset is not None
    
"""Test error handling for adding item to cart"""
def test_error_add_to_cart(client):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    with patch('app.extensions.db.session.commit', side_effect=Exception("Database commit failed")):
    
        response = client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
        assert b'Item failed to add.' in response.data

"""Test viewing items in cart"""
def test_viewing_cart(client):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
   
    response = client.get ("/view_cart",follow_redirects=True)
    assert b'<td>Ship</td>' in response.data

"""Test error handling when viewing cart"""
def test_error_viewing_cart(client, monkeypatch):
    class FakeAssetsQuery:
        @staticmethod
        def filter(*args, **kwargs):
            raise Exception("Database query failed")
    monkeypatch.setattr(Cart, 'query', FakeAssetsQuery)
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get ("/view_cart",follow_redirects=True)
    assert b'An error occurred retrieving assets.' in response.data

"""Test checking out cart and creating an order."""
def test_check_out(client,app):  
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    
    response = client.post ("/checkout", follow_redirects=True)
    assert b'Your order has been placed successfully.' in response.data
    
    with app.app_context():
            order=Order.query.filter_by(asset_id='1').first()
            assert order is not None 

"""Test error handling on checking out item"""
def test_error_check_out(client,app):  
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    
    with patch('app.extensions.db.session.commit', side_effect=Exception("Database commit failed")):
    
        response = client.post ("/checkout", follow_redirects=True)
        assert b'Order failed to place.' in response.data
        
        with app.app_context():
                order=Order.query.filter_by(asset_id='1').first()
                assert order is None 

"""Test removing item from cart"""
def test_remove_cart_item(client,app): 
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    response = client.post(f"/remove_item/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    assert b'Item was successfully removed from cart.' in response.data
        
"""Test error handling for removing item from cart"""
def test_error_remove_cart_item(client):
        client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
        asset = Assets.query.filter_by(asset_name='Ship').first()
        client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
        with patch('app.models.models.db.session.delete', side_effect=Exception("Database commit failed")):
        
            response = client.post(f"/remove_item/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
            assert b'Item failed to remove from cart' in response.data

"""Test item not found in  cart"""
def test_notfound_cart_item(client,app): 
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    response = client.post(f"/remove_item/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    assert b'Item not found in cart.' in response.data
       
"""Test viewing order history"""
def test_view_order_history(client):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post ("/checkout", follow_redirects=True)
    
    response = client.get ("/order_history",follow_redirects=True)
    assert b'<td>Ship</td>' in response.data
    assert b'<td>Order Placed</td>' in response.data        

"""Test error handling when viewing order history"""
def test_error_viewing_order_history(client, monkeypatch):
    class FakeAssetsQuery:
        @staticmethod
        def filter(*args, **kwargs):
            raise Exception("Database query failed")
    monkeypatch.setattr(Order, 'query', FakeAssetsQuery)
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    response = client.get ("/order_history",follow_redirects=True)
    assert b'An error occurred retrieving assets.' in response.data
    
"""Test returning an asset"""
def test_return_asset(client, app):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post("/checkout", follow_redirects=True)
    client.get("/return_asset/", follow_redirects=True)
   
    order = Order.query.filter_by(username='testuser', asset_id=asset.asset_id).first()
    response = client.post("/return_asset/", data={"order_id": order.order_id, "asset_id": asset.asset_id}, follow_redirects=True)
    assert b"Item returned successfully." in response.data
  
"""Test error handling for returning an asset"""
def test_error_return_asset(client, app):
    client.post("/", data={"username": "testuser", "password": "Assignment1/"}, follow_redirects=True)
    asset = Assets.query.filter_by(asset_name='Ship').first()
    client.post(f"/add_to_cart/{asset.asset_id}", data={"asset_id": asset.asset_id}, follow_redirects=True)
    client.post("/checkout", follow_redirects=True)
    client.get("/return_asset/", follow_redirects=True)
    with patch('app.extensions.db.session.commit', side_effect=Exception("Database commit failed")):
        order = Order.query.filter_by(username='testuser', asset_id=asset.asset_id).first()
        response = client.post("/return_asset/", data={"order_id": order.order_id, "asset_id": asset.asset_id}, follow_redirects=True)
        assert b"Item failed to return." in response.data