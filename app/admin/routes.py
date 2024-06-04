from functools import wraps
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.admin import bp
from app.extensions import db
from app.models.models import User, Branch


#Function checks if user is of the role admin when attempting to access centain functions. 
#If they are not it will return them to the reserve_parking page and put a line in the log.
def check_is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            current_app.logger.critical('Username: %s accessed attempted to access %s', current_user.username,func.__name__)
            flash("You are not authorised to access this page")
            return redirect(url_for("main.home"))
    return decorated_function

def get_branch_details(branches):
    branch_names = {}
    for branch in branches:
        branch = Branch.query.filter_by(branch_id=branch.branch_id).first()
        if branch:
            branch_names[branch.branch_id] = branch.branch_name
    return branch_names

#Function to return all user account when you are loggined in as a admin user.
@bp.route("/maintain_user", methods=['GET'])
@login_required
@check_is_admin
def maintain_user():
    try: 
        admins = User.query.all()
        current_app.logger.info('Username: %s access maintain users', current_user.username)
        branch_names = get_branch_details(admins)
        return render_template('maintain_user.html', admins=admins, branch_names=branch_names)
    except Exception as e: 
        flash("An error occurred retrieving users.")
        current_app.logger.warning('There was an error retrieving users on maintain users')
        return redirect(url_for('main.home'))
    
#Function to be able to edit a username or role
@bp.route("/edit_user/<int:id>", methods=['GET','POST'])
@login_required
@check_is_admin
def edit_user(id):
    admin = User.query.filter_by(id=id).first()
    branch_names = {}
    if admin:
            branch = Branch.query.filter_by(branch_id=admin.branch_id).first()
            if branch:
                branch_names[admin.branch_id] = branch.branch_name

    if request.method == "POST":
        current_app.logger.info('Username: %s accessed edit_user', current_user.username)
        admin.username = request.form['username']
        admin.branch_name = request.form['branch_name']
        admin.role = request.form['role']
        admin.authorised = request.form['authorised']

        #Save update to database
        try:
            db.session.commit()
            current_app.logger.info('Username: %s updated user account %s', current_user.username, admin.username)
            flash("User updated successfully")
            return redirect(url_for("admin.maintain_user"))
        except Exception as e:
            flash("User failed to update")
            current_app.logger.warning('Username: %s failed to update user account %s', current_user.username, admin.username)
            return render_template("edit_user.html", admin=admin,branch_names=branch_names)
            
    else:
        return render_template("edit_user.html", admin=admin,branch_names=branch_names)


#Function to delete  users.
@bp.route("/delete_user/", methods=['GET', 'POST'])
@login_required
@check_is_admin
def delete_user():
    id = request.form.get("id")
    delete_user = User.query.filter_by(id=id).first()

    try:
        db.session.delete(delete_user)
        current_app.logger.info('Username: %s deleted %s account', current_user.username, delete_user.username)
        db.session.commit()
        flash("User was deleted successfully.")
        return redirect(url_for("admin.maintain_user"))
    except Exception as e:
        flash("User failed to delete.")
        current_app.logger.warning('Username: %s failed to deleted an account', current_user.username)
        return render_template("maintain_user.html")

@bp.route("/maintain_branch")
@login_required
@check_is_admin
def maintain_branch():
    try: 
        branch= Branch.query.all()
        current_app.logger.info('Username: %s accessed maintain branches', current_user.username)
        return render_template('maintain_branch.html',branch=branch)
    except Exception as e: 
        flash("An error occurred retrieving branches.")
        current_app.logger.warning('Error during retrieving all users: %s', str(e))
        return redirect(url_for('main.home'))

@bp.route("/add_branch",methods=['GET','POST'])
@login_required
@check_is_admin
def add_branch():
    if request.method == "POST":
        add_branch = Branch(branch_name=request.form.get("branch_name"),address_line1=request.form.get("address_line1"), address_line2=request.form.get("address_line2"),postcode=request.form.get("postcode"))
        try:
            db.session.add(add_branch)
            db.session.commit()
            current_app.logger.info('Username: %s created a new branch', current_user.username)
            flash("Branch added successfully.")
            return redirect(url_for("admin.maintain_branch"))
        except Exception as e:
            flash("Branch failed to create.")
            current_app.logger.warning('Username: %s had a failure when creating a new branch', current_user.username)
            return redirect(url_for("admin.maintain_branch"))
    else:
        return render_template("add_branch.html")
            
    
@bp.route("/edit_branch/<int:branch_id>", methods=['GET','POST'])
@login_required
@check_is_admin
def edit_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id) 

    if request.method == "POST":
        current_app.logger.info('Username: %s accessed edit_branch', current_user.username)
        branch.branch_name = request.form['branch_name']
        branch.address_line1 = request.form['address_line1']
        branch.address_line2 = request.form['address_line2']
        branch.postcode = request.form['postcode']

        #Save update to database
        try:
            db.session.commit()
            current_app.logger.info('Username: %s updated branch %s', current_user.username, branch.branch_id)
            flash("Branch updated successfully")
            return redirect(url_for("admin.maintain_branch"))
        except Exception as e:
            flash("Branch failed to update")
            current_app.logger.warning('Username: %s failed to update branch %s', current_user.username, branch.branch_id)
            return redirect(url_for("admin.maintain_branch"))
            
    else:
        return render_template("edit_branch.html", branch=branch)
    
@bp.route("/delete_branch/", methods=['GET', 'POST'])
@login_required
@check_is_admin
def delete_branch():
    branch_id = request.form.get("branch_id")
    delete_branch = Branch.query.filter_by(branch_id=branch_id).first()

    try:
        db.session.delete(delete_branch)
        current_app.logger.info('Username: %s deleted %s branch', current_user.username, delete_branch.branch_id)
        db.session.commit()
        flash("Branch was deleted successfully.")
        return redirect(url_for("admin.maintain_branch"))
    except Exception as e:
        flash("Branch failed to delete.")
        current_app.logger.warning('Username: %s failed to deleted branch', current_user.username)
        return redirect(url_for("admin.maintain_branch"))
    
#Function to return logged messages
@bp.route('/logging_messages')
@login_required
@check_is_admin
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