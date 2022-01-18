# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from TrackerApp import db
from TrackerApp.models import User 
from TrackerApp.users.forms import RegistrationForm, LoginForm 

users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



# login
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            
            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('jobs.list_jobs')

            return redirect(next)
        else:
            flash('Password incorrect!')

    return render_template('login.html',form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


