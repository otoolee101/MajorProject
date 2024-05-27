
import pytest
from app.extensions import db, bcrypt
from app.models.models import User

"""Test login page appears"""
def test_login_page(client):
    response = client.get('/')
    assert b'<h1>Login Page</h1>' in response.data
