from flask import flash, redirect, render_template, request, url_for
from app.admin import bp
from app.extensions import db
from app.models.models import User, assets

@bp.route("/maintain_assets")
def maintain_assets():
    try: 
        asset= assets.query.all()
        #current_app.logger.info('Username: %s accessed admin', current_user.username)
        return render_template('maintain_assets.html',asset=asset)
    except Exception as e: 
        flash("An error occurred retrieving assets.")
        #current_app.logger.exception('Error during retrieving all users: %s', str(e))
    return render_template("home.html")

@bp.route("/add_asset",methods=["GET", "POST"])
def add_asset():
    if request.method == "POST":
        add_asset = assets(asset_name=request.form.get("asset_name"),asset_description=request.form.get("asset_description"),keyword=request.form.get("keyword"))

        try:
            db.session.add(add_asset)
            db.session.commit()
            # current_app.logger.info('Username: %s created a new booking in reserve_parking', current_user.username)
            flash("Asset added successfully.")
            return redirect(url_for("admin.maintain_assets"))
        except Exception as e:
            flash("Asset failed to create. Please contact system administration.")
            # current_app.logger.exception('Username: %s had a failure when creating a booking for reserve_parking: %s', current_user.username)
            return render_template("main/home.html")
    
    return render_template("add_asset.html")

@bp.route("/edit_asset/<int:asset_id>", methods=['POST', 'GET'])
def edit_asset(asset_id):
    edit = assets.query.get_or_404(asset_id)
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
            return redirect(url_for('admin.maintain_assets'))
        except Exception as e:
            flash("Asset failed to update")
            #current_app.logger.warning('Username: %s failed to edit a reservation %s', current_user.username, edit.id)
            return redirect(url_for('admin.maintain_assets', edit=edit))
    else:
            #current_app.logger.warning('Username: %s failed to access reservations', current_user.username)
            return render_template("edit_asset.html", edit=edit)  

#Function to delete  users.
@bp.route("/delete_asset/", methods=['POST'])
def delete_asset():
    asset_id = request.form.get("asset_id")
    delete_asset = assets.query.filter_by(asset_id=asset_id).first()

    try:
        db.session.delete(delete_asset)
        #current_app.logger.warning('Username: %s deleted %s account', current_user.username, delete_user.username)
        db.session.commit()
        flash("Asset was deleted successfully.")
        return redirect(url_for("admin.maintain_assets"))
    except Exception as e:
        flash("Asset failed to delete.")
        #current_app.logger.warning('Username: %s failed to deleted an account', current_user.username)
        return render_template("maintain_assets.html")

#Function to return all user account when you are loggined in as a admin user.
@bp.route("/maintain_user")
def maintain_user():
    try: 
        admin= User.query.all()
        #current_app.logger.info('Username: %s accessed admin', current_user.username)
        return render_template('maintain_user.html',admin=admin)
    except Exception as e: 
        flash("An error occurred retrieving users.")
        #current_app.logger.exception('Error during retrieving all users: %s', str(e))
        return redirect(url_for('main.home'))

    
#Function to be able to edit a username or role
@bp.route("/edit_user/<int:user_id>", methods=['GET','POST'])
def edit_user(user_id):
    admin = User.query.get_or_404(user_id) 

    if request.method == "POST":
        #current_app.logger.info('Username: %s accessed edit_user', current_user.username)
        admin.username = request.form['username']
        admin.registration = request.form['registration']
        admin.role = request.form['role']
        admin.authorised = request.form['authorised']

        #Save update to database
        try:
            db.session.commit()
           # current_app.logger.info('Username: %s updated user account %s', current_user.username, admin.username)
            flash("User updated successfully")
            return redirect(url_for("admin.maintain_user"))
        except Exception as e:
            #current_app.logger.exception(e)
            flash("User failed to update")
           # current_app.logger.warning('Username: %s failed to update user account %s', current_user.username, admin.username)
            return render_template("edit_user.html", admin=admin)
            
    else:
        return render_template("edit_user.html", admin=admin)

#Function to delete  users.
@bp.route("/delete_user/", methods=['GET', 'POST'])
def delete_user():
    user_id = request.form.get("user_id")
    delete_user = User.query.filter_by(user_id=user_id).first()

    try:
        db.session.delete(delete_user)
        #current_app.logger.warning('Username: %s deleted %s account', current_user.username, delete_user.username)
        db.session.commit()
        flash("User was deleted successfully.")
        return redirect(url_for("admin.maintain_user"))
    except Exception as e:
        flash("User failed to delete.")
        #current_app.logger.warning('Username: %s failed to deleted an account', current_user.username)
        return render_template("maintain_user.html")
    
#Function to return logged messages
@bp.route('/logging_messages')
def logging_messages():
        log_file_path = 'app.log'
        log_content = read_log_file(log_file_path)

        return render_template('logging_messages.html', log_content=log_content)
   
def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            log_content = file.read()
        return log_content
    
    except FileNotFoundError:
        return "Log file not found"