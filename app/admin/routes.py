from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.admin import bp
from app.extensions import db
from app.models.models import User, Assets, Order

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

    
#Function to be able to edit a username or role
@bp.route("/edit_user/<int:id>", methods=['GET','POST'])
@login_required
def edit_user(id):
    admin = User.query.get_or_404(id) 

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
@login_required
def delete_user():
    id = request.form.get("id")
    delete_user = User.query.filter_by(id=id).first()

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
@login_required
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