from flask import Blueprint

bp = Blueprint('manager', __name__, template_folder='templates')

from app.manager import routes