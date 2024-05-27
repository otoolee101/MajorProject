from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.manager import bp
from app.extensions import db
from app.models.models import User, Assets, Order, Branch

@bp.route("/maintain_assets")
@login_required
def maintain_assets():
    try: 
        asset= Assets.query.all()
        #current_app.logger.info('Username: %s accessed admin', current_user.username)
        return render_template('maintain_assets.html',asset=asset)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        #current_app.logger.exception('Error during retrieving all users: %s', str(e))
    return render_template("home.html")

@bp.route("/add_asset",methods=["GET", "POST"])
@login_required
def add_asset():
    if request.method == "POST":
        add_asset = Assets(asset_name=request.form.get("asset_name"),asset_description=request.form.get("asset_description"),keyword=request.form.get("keyword"))

        try:
            db.session.add(add_asset)
            db.session.commit()
            # current_app.logger.info('Username: %s created a new booking in reserve_parking', current_user.username)
            flash("Asset added successfully.")
            return redirect(url_for("manager.maintain_assets"))
        except Exception as e:
            flash("Asset failed to create. Please contact system administration.")
            # current_app.logger.exception('Username: %s had a failure when creating a booking for reserve_parking: %s', current_user.username)
            return render_template("main/home.html")
    
    return render_template("add_asset.html")

@bp.route("/edit_asset/<int:asset_id>", methods=['POST', 'GET'])
@login_required
def edit_asset(asset_id):
    edit = Assets.query.get_or_404(asset_id)
    if request.method == "POST":
        #current_app.logger.info('Username: %s accessed edit reservation', current_user.username)
        edit.asset_name = request.form['asset_name']
        edit.asset_description = request.form['asset_description']
        edit.keyword = request.form['keyword']
        edit.available = request.form['available']

        #Save update to database
        try:
            db.session.commit()
            #current_app.logger.info('Username: %s edited a reservation %s', current_user.username, edit.id)
            flash("Asset updated successfully")
            return redirect(url_for('manager.maintain_assets'))
        except Exception as e:
            flash("Asset failed to update")
            #current_app.logger.warning('Username: %s failed to edit a reservation %s', current_user.username, edit.id)
            return redirect(url_for('manager.maintain_assets', edit=edit))
    else:
            #current_app.logger.warning('Username: %s failed to access reservations', current_user.username)
            return render_template("edit_asset.html", edit=edit)  

#Function to delete  users.
@bp.route("/delete_asset/", methods=['POST'])
@login_required
def delete_asset():
    asset_id = request.form.get("asset_id")
    delete_asset = Assets.query.filter_by(asset_id=asset_id).first()

    try:
        db.session.delete(delete_asset)
        #current_app.logger.warning('Username: %s deleted %s account', current_user.username, delete_user.username)
        db.session.commit()
        flash("Asset was deleted successfully.")
        return redirect(url_for("manager.maintain_assets"))
    except Exception as e:
        flash("Asset failed to delete.")
        #current_app.logger.warning('Username: %s failed to deleted an account', current_user.username)
        return redirect(url_for("manager.maintain_assets"))

#Function to return all user account when you are loggined in as a admin user.
@bp.route("/maintain_user")
@login_required
def maintain_user():
    try: 
        admin= User.query.all()
        #current_app.logger.info('Username: %s accessed admin', current_user.username)
        return render_template('maintain_user.html',admin=admin)
    except Exception as e: 
        flash("An error occurred retrieving users.")
        #current_app.logger.exception('Error during retrieving all users: %s', str(e))
        return redirect(url_for('main.home'))

@bp.route("/asset_history/<int:asset_id>", methods=['GET'])
@login_required
def asset_history(asset_id):
    try: 
        asset_history_items = Order.query.filter_by(asset_id=asset_id).all()
        # Create a dictionary to store asset names
        asset_names = {}
        asset_description = {}
        branch_names = {}
        # Fetch asset names corresponding to asset IDs in the cart
        for item in asset_history_items:
            asset = Assets.query.filter_by(asset_id=item.asset_id).first()
            branch = Branch.query.filter_by(branch_id=item.branch_id).first()
            if asset:
                asset_names[item.asset_id] = asset.asset_name
                asset_description[item.asset_id] = asset.asset_description
                branch_names[item.branch_id] = branch.branch_name
    except Exception as e: 
        flash("An error occurred retrieving assets.")
    return render_template("asset_history.html", asset_history_items=asset_history_items, 
                           asset_names=asset_names, 
                           asset_description=asset_description, branch_names=branch_names)

@bp.route("/maintain_orders/", methods=['GET'])
@login_required
def maintain_orders():
    try: 
        order = Order.query.all()
        # Create a dictionary to store asset names
        asset_names = {}
        asset_description = {}
        branch_names = {}
        # Fetch asset names corresponding to asset IDs in the cart
        for item in order:
            asset = Assets.query.filter_by(asset_id=item.asset_id).first()
            branch = Branch.query.filter_by(branch_id=item.branch_id).first()
            if asset:
                asset_names[item.asset_id] = asset.asset_name
                asset_description[item.asset_id] = asset.asset_description
                branch_names[item.branch_id] = branch.branch_name
    except Exception as e: 
        flash("An error occurred retrieving assets.")
    return render_template("maintain_orders.html", order=order, 
                           asset_names=asset_names, 
                           asset_description=asset_description,branch_names=branch_names)


@bp.route("/edit_order/<int:order_id>", methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    asset_names = {}
    asset_description = {}
    branch_names = {}

    # Fetch asset and branch information
    asset = Assets.query.filter_by(asset_id=order.asset_id).first()
    if asset:
        asset_names[order.asset_id] = asset.asset_name
        asset_description[order.asset_id] = asset.asset_description

    branch = Branch.query.filter_by(branch_id=order.branch_id).first()
    if branch:
        branch_names[branch.branch_id] = branch.branch_name

    if request.method == "POST":
        # Update order status
        order.status = request.form['status']
        try:
            db.session.commit()
            flash("Order updated successfully")
        except Exception as e:
            flash("An error occurred while updating order status: " + str(e))
        return redirect(url_for('manager.maintain_orders'))

    # Render the template for both GET and POST requests
    return render_template("edit_order.html", order=order, 
                           asset_names=asset_names, 
                           asset_description=asset_description,
                           branch_names=branch_names)
