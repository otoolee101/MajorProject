from functools import wraps
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.manager import bp
from app.extensions import db
from app.models.models import Assets, Order, Branch

#Function to check the user role is admin or manager before they are allowed to access the function. 
def check_is_manager(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role == 'admin'or current_user.role == 'manager':
            return func(*args, **kwargs)
        else:
            current_app.logger.critical('Username: %s accessed attempted to access %s', current_user.username,func.__name__)
            flash("You are not authorised to access this page")
            return redirect(url_for("main.home"))
    return decorated_function

#Function gets the details associated with the id of the asset or branch to display a meaningful title/description on the website. 
def get_asset_details(item_deatils):
    asset_names = {}
    asset_description = {}
    branch_names = {}

    for item in item_deatils:
        asset = Assets.query.filter_by(asset_id=item.asset_id).first()
        branch = Branch.query.filter_by(branch_id=item.branch_id).first()
        if asset:
            asset_names[item.asset_id] = asset.asset_name
            asset_description[item.asset_id] = asset.asset_description
        if branch:
            branch_names[item.branch_id] = branch.branch_name

    return asset_names, asset_description, branch_names


#view all assets in a single screen
@bp.route("/maintain_assets")
@login_required
@check_is_manager
def maintain_assets():
    try: 
        asset= Assets.query.all()
        current_app.logger.info('Username: %s accessed maintain assets', current_user.username)
        return render_template('maintain_assets.html',asset=asset)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        current_app.logger.warning('Error during retrieving all assets: %s', str(e))
    return render_template("home.html")

#Function to create a new asset
@bp.route("/add_asset",methods=["GET", "POST"])
@login_required
@check_is_manager
def add_asset():
    if request.method == "POST":
        add_asset = Assets(asset_name=request.form.get("asset_name"),asset_description=request.form.get("asset_description"),keyword=request.form.get("keyword"))

        try:
            db.session.add(add_asset)
            db.session.commit()
            current_app.logger.info('Username: %s created a asset %s', current_user.username, add_asset.asset_name)
            flash("Asset added successfully.")
            return redirect(url_for("manager.maintain_assets"))
        except Exception as e:
            flash("Asset failed to create. Please contact system administration.")
            current_app.logger.exception('Username: %s had a failure when creating a new asset', current_user.username)
            return redirect(url_for("manager.maintain_assets"))
    
    return render_template("add_asset.html")

#Function to edit an asset and make it available or not.
@bp.route("/edit_asset/<int:asset_id>", methods=['POST', 'GET'])
@login_required
@check_is_manager
def edit_asset(asset_id):
    edit = Assets.query.get_or_404(asset_id)
    if request.method == "POST":
        current_app.logger.info('Username: %s accessed edit asset', current_user.username)
        edit.asset_name = request.form['asset_name']
        edit.asset_description = request.form['asset_description']
        edit.keyword = request.form['keyword']
        edit.available = request.form['available']
        try:
            db.session.commit()
            flash("Asset updated successfully")
            current_app.logger.info('Username: %s edited asset %s', current_user.username, edit.asset_id)
            return redirect(url_for('manager.maintain_assets'))
        except Exception as e:
            flash("Asset failed to update")
            current_app.logger.warning('Username: %s failed to edit asset %s', current_user.username, edit.asset_id)
            return redirect(url_for('manager.maintain_assets'))
    else:
            current_app.logger.warning('Username: %s failed to access assets', current_user.username)
            return render_template("edit_asset.html", edit=edit)  

#Function to delete assets.
@bp.route("/delete_asset/", methods=['POST'])
@login_required
@check_is_manager
def delete_asset():
    asset_id = request.form.get("asset_id")
    delete_asset = Assets.query.filter_by(asset_id=asset_id).first()

    try:
        if delete_asset is None:
            flash("Asset not found.")
            current_app.logger.critical('Username: %s tried to delete asset with id %s that does not exist', current_user.username, asset_id)
            return redirect(url_for("manager.maintain_assets"))

        db.session.delete(delete_asset)
        db.session.commit()
        current_app.logger.info('Username: %s deleted asset %s', current_user.username, asset_id)
        flash("Asset was deleted successfully.")
    except Exception as e:
        db.session.rollback()
        current_app.logger.warning('Username: %s failed to delete asset %s due to error: %s', current_user.username, asset_id, str(e))
        flash("Asset failed to delete.")
    
    return redirect(url_for("manager.maintain_assets"))

#Function to see all the history of a single asset
@bp.route("/asset_history/<int:asset_id>", methods=['GET'])
@login_required
@check_is_manager
def asset_history(asset_id):
    try: 
        asset_history_items = Order.query.filter_by(asset_id=asset_id).all()
        #Call get_asset_details to display meaniful decriptions
        asset_history = asset_history_items
        asset_names, asset_description, branch_names = get_asset_details(asset_history)
        current_app.logger.info('Username: %s accessed asset %s history', current_user.username, asset_id)

    except Exception as e: 
        flash("An error occurred retrieving assets.")
        asset_history_items = {}
        asset_names = {}
        asset_description = {}
        branch_names = {}
        current_app.logger.warning('Username: %s has a problem accessing asset history', current_user.username)

    return render_template("asset_history.html", 
                           asset_history_items=asset_history_items, asset_names=asset_names,
                           asset_description=asset_description, branch_names=branch_names)


#Function to see all orders that have been created. 
@bp.route("/maintain_orders/", methods=['GET'])
@login_required
@check_is_manager
def maintain_orders():
    try:
        new_order = Order.query.filter(Order.status == 'Order Placed').all()
        active_order = Order.query.filter(Order.status.in_(['Order Shipped', 'Order Delivered'])).all()
        past_order = Order.query.filter(Order.status == 'Returned').all()
        current_app.logger.info('Username: %s accessed maintain orders', current_user.username)
        
        orders = new_order + active_order + past_order
        asset_names, asset_description, branch_names = get_asset_details(orders)

    except Exception as e:
        flash(f"An error occurred retrieving orders.")
        current_app.logger.warning('Username: %s had a problem accessing maintain orders', current_user.username)
        new_order = []
        active_order = []
        past_order = []
        asset_names = {}
        asset_description = {}
        branch_names = {}
        return redirect(url_for("main.home"))
    
    return render_template("maintain_orders.html", new_order=new_order, active_order=active_order,past_order=past_order,
                           asset_names=asset_names, asset_description=asset_description,branch_names=branch_names)

#Function to edit the status of an order. 
@bp.route("/edit_order/<int:order_id>", methods=['GET', 'POST'])
@login_required
@check_is_manager
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    asset_names, asset_description, branch_names = get_asset_details([order])
    current_app.logger.info('Username: %s accessed edit order %s', current_user.username, order.order_id)
   
    if request.method == "POST":
        order.status = request.form['status']
        try:
            db.session.commit()
            flash("Order updated successfully")
            current_app.logger.info('Username: %s edited order %s', current_user.username, order.order_id)
            return redirect(url_for("manager.maintain_orders"))
        
        except Exception as e:
            flash("An error occurred while updating order status")
            current_app.logger.warning('Username: %s had a problem editing order %s', current_user.username, order.order_id)
            return redirect(url_for("manager.maintain_orders"))
            
    return render_template("edit_order.html", order=order, 
                           asset_names=asset_names, 
                           asset_description=asset_description,
                           branch_names=branch_names)

