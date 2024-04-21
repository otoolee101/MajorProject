from flask import flash, render_template
from app.main import bp
from app.models.models import assets

@bp.route("/home")
def home():
    return render_template("home.html")

@bp.route("/return_asset")
def return_asset():
    return render_template("return_asset.html")

@bp.route("/borrow_asset")
def borrow_asset():
    try: 
        asset= assets.query.all()
        #current_app.logger.info('Username: %s accessed admin', current_user.username)
        return render_template('borrow_asset.html',asset=asset)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        #current_app.logger.exception('Error during retrieving all users: %s', str(e))
    return render_template("home.html")

@bp.route("/order_history")
def order_history():
    return render_template("order_history.html")

@bp.route("/cart")
def cart():
    return render_template("cart.html")