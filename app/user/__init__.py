from flask import Blueprint

bp = Blueprint('user', __name__, template_folder='templates')

from app.user import routes