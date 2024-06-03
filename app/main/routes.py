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

@bp.route("/return_asset/", methods=['GET', 'POST'])
@login_required
def return_asset():
    try:
        return_assets = Order.query.filter(Order.username == current_user.username, Order.status != 'Returned').all()
        current_date = datetime.now()
        asset_names = {}
        asset_descriptions = {}
        
        for return_asset in return_assets:
            asset = Assets.query.filter_by(asset_id=return_asset.asset_id).first()
            if asset:
                asset_names[return_asset.asset_id] = asset.asset_name
                asset_descriptions[return_asset.asset_id] = asset.asset_description

        if request.method == "POST":
            order_id = request.form.get('order_id')
            asset_id = request.form.get('asset_id')
            return_asset = Order.query.filter_by(order_id=order_id).first()
            update_asset = Assets.query.filter_by(asset_id=asset_id).first()
            if return_asset:
                return_asset.status = 'Returned'
                return_asset.return_date = current_date
                update_asset.available = 'Y'
                try:
                    db.session.commit()
                    flash("Item returned successfully.")
                    return redirect(url_for("main.home"))
                except Exception as e:
                    flash("Item failed to return.")
                    return redirect(url_for('main.home'))

        return render_template('return_asset.html', return_assets=return_assets, asset_names=asset_names, asset_descriptions=asset_descriptions)
    except Exception as e:
        flash("Error returning Item.")
        return redirect(url_for("main.home"))


@bp.route("/borrow_asset")
@login_required
def borrow_asset():
    try: 
        assets = Assets.query.filter(Assets.available == 'Y').all()
        return render_template('borrow_asset.html', assets=assets)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        return redirect(url_for("main.home"))
                  
@bp.route('/add_to_cart/<int:asset_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(asset_id):
    if request.method == "POST": 
        add_item = Cart(username=current_user.username, asset_id=request.form.get("asset_id"), branch_id=current_user.branch_id)
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
                    branch_id=current_user.branch_id,
                    check_out_date=current_date,
                    status='Order Placed'
                )
                db.session.add(order)
                remove_item(cart_item.asset_id, checked_out=True)
            
            db.session.commit()
            flash("Your order has been placed successfully.")
            return redirect(url_for("main.home"))
        except Exception as e:
            db.session.rollback()
            flash("Order failed to place.")
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

@bp.route("/order_history")
@login_required
def order_history():
    try: 
        current_order_history = Order.query.filter(Order.username == current_user.username, Order.status != 'Returned').all()
        past_order_history = Order.query.filter(Order.username == current_user.username,Order.status == 'Returned').all()
        # Create a dictionary to store asset names
        asset_names = {}
        asset_description = {}
        # Fetch asset names corresponding to asset IDs in the cart
        for item in current_order_history + past_order_history :
            asset = Assets.query.filter_by(asset_id=item.asset_id).first()
            if asset:
                asset_names[item.asset_id] = asset.asset_name
                asset_description[item.asset_id] = asset.asset_description

        return render_template('order_history.html', current_order_history=current_order_history, asset_names=asset_names,asset_description=asset_description, past_order_history=past_order_history)
    except Exception as e: 
        flash("An error occurred retrieving orders.")
    return redirect(url_for("main.home"))

