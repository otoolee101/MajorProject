from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.main import bp
from app.models.models import Assets, Cart, Order
from app.extensions import db

@bp.route("/home")
@login_required
def home():
    return render_template("home.html")

@bp.route("/return_asset")
@login_required
def return_asset():
    return render_template("return_asset.html")

@bp.route("/borrow_asset")
@login_required
def borrow_asset():
    try: 
        assets = Assets.query.filter(Assets.available == 'Y').all()
        return render_template('borrow_asset.html', assets=assets)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        return render_template("home.html")
                  
@bp.route('/add_to_cart/<int:asset_id>', methods=['GET', 'POST'])
def add_to_cart(asset_id):
    if request.method == "POST": 
        add_item = Cart(username=current_user.username, asset_id=request.form.get("asset_id"), branch_name=current_user.branch_name)
        available = Assets.query.filter_by(asset_id=asset_id).first()
        try:
            available.available = 'N'
            db.session.add(add_item)
            db.session.commit()
            flash("Item added successfully.")
            return redirect(url_for("main.borrow_asset"))
        except:
            flash("Item failed to add.")
            return redirect(url_for('main.home'))
  
@bp.route("/order_history")
@login_required
def order_history():
    try: 
        order_history = Order.query.filter(Order.username == current_user.username).all()
        # Create a dictionary to store asset names
        asset_names = {}
        asset_description = {}
        # Fetch asset names corresponding to asset IDs in the cart
        for item in order_history:
            asset = Assets.query.filter_by(asset_id=item.asset_id).first()
            if asset:
                asset_names[item.asset_id] = asset.asset_name
                asset_description[item.asset_id] = asset.asset_description

        return render_template('order_history.html', order_history=order_history, asset_names=asset_names,asset_description=asset_description)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
    return redirect(url_for("main.home"))

@bp.route("/view_cart")
@login_required
def view_cart():
    try: 
        view_cart = Cart.query.filter(Cart.username == current_user.username).all()
        # Create a dictionary to store asset names
        asset_names = {}
        asset_description = {}
        # Fetch asset names corresponding to asset IDs in the cart
        for item in view_cart:
            asset = Assets.query.filter_by(asset_id=item.asset_id).first()
            if asset:
                asset_names[item.asset_id] = asset.asset_name
                asset_description[item.asset_id] = asset.asset_description

        return render_template('cart.html', view_cart=view_cart, asset_names=asset_names,asset_description=asset_description)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        return render_template("home.html")

@bp.route("/checkout", methods=['POST'])
@login_required
def checkout():
    if request.method == "POST": 
        current_date = datetime.now()
        cart_items = Cart.query.filter(Cart.username == current_user.username).all()
        
        try:
            for cart_item in cart_items: 
                order = Order(
                    username=current_user.username,
                    asset_id=cart_item.asset_id,
                    branch_name=current_user.branch_name,
                    date=current_date,
                    status='Order Placed'
                )
                db.session.add(order)
                remove_item(cart_item.asset_id, checked_out=True)
            
            db.session.commit()
            flash("Your order has been placed successfully.")
            return redirect(url_for("main.home"))
        except Exception as e:
            db.session.rollback()
            flash(f"Order failed to place: {str(e)}")
            return redirect(url_for('main.home'))

@bp.route("/remove_item/<int:asset_id>", methods=['POST'])
@login_required
def remove_item(asset_id,checked_out=False):
    try:
        remove_item = Cart.query.filter_by(asset_id=asset_id, username=current_user.username).first()
        available = Assets.query.filter_by(asset_id=asset_id).first()
        if remove_item:
            db.session.delete(remove_item)
            if checked_out: 
                db.session.commit()
            else:
                flash("Item was successfully removed from cart.")
                available.available = 'Y'
                db.session.commit()
        else:
            flash("Item not found in cart.")
    except Exception as e:
        flash("Item failed to remove from cart")

    return redirect(url_for("main.view_cart"))

