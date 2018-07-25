from flask import (
        Blueprint, redirect, render_template,
        Response, request, url_for
)
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from project import db
from project.forms import RegisterForm, LoginForm
from project.models import User


users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    # TODO: Fill this in!
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user != None:
                return Response ("<p> account already exists <p>")
                return render_template('register.html', form=form)
            else:
                print(email)
                print(name)
                print(password)
                user = User(email=email, name= name, password= password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('browse.html'))
    else:
        return render_template('register.html', form=form)
   
                

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is None or not user.check_password(password):
                return Response("<p>Incorrect email or password</p>")
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('private_route')
            return redirect(next_page)
        else:
            return Response("<p>invalid form</p>")
    return render_template('login.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return Response("<p>Logged out</p>")
