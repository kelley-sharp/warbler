import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from forms import UserForm, LoginForm, MessageForm
from decorators import ensure_correct_user

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/warbler_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "it's a secret"
toolbar = DebugToolbarExtension(app)

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Message


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.login_view = "users_login"


# Users routes
@app.route('/users', methods=["GET"])
def users_index():
    search = request.args.get('q')
    users = None
    if search is None or search == '':
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()
    return render_template('users/index.html', users=users)


@app.route('/signup', methods=["GET"])
def users_new():
    return render_template('users/signup.html', form=UserForm())


@app.route('/signup', methods=["POST"])
def users_create():
    form = UserForm()
    if form.validate():
        try:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=User.hash_password(form.password.data))
            if form.image_url.data:
                new_user.image_url = form.image_url.data
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('root'))
        except IntegrityError as e:
            flash({'text': "Username already taken", 'status': 'danger'})
    return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET"])
def users_login():
    return render_template('users/login.html', form=LoginForm())


@app.route('/login', methods=["POST"])
def users_login_create():
    form = LoginForm()
    if form.validate():
        found_user = User.authenticate(form.username.data, form.password.data)
        if found_user:
            login_user(found_user)
            flash({
                'text': f"Hello, {found_user.username}!",
                'status': 'success'
            })
            return redirect(url_for('root'))
        flash({'text': "Invalid credentials.", 'status': 'danger'})
    return render_template('users/login.html', form=form)


@app.route('/logout')
@login_required
def users_logout():
    logout_user()
    flash({'text': "You have successfully logged out.", 'status': 'success'})
    return redirect(url_for('users_login'))


@app.route('/users/<int:follower_id>/followers', methods=['POST'])
@login_required
def followers_create(follower_id):
    followed = User.query.get(follower_id)
    current_user.following.append(followed)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('users_following', user_id=current_user.id))


@app.route('/users/<int:follower_id>/followers', methods=['DELETE'])
@login_required
def followers_destroy(follower_id):
    followed = User.query.get(follower_id)
    current_user.following.remove(followed)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('users_following', user_id=current_user.id))


@app.route('/users/<int:user_id>/following', methods=['GET'])
@login_required
def users_following(user_id):
    return render_template(
        'users/following.html', user=User.query.get(user_id))


@app.route('/users/<int:user_id>/followers', methods=['GET'])
@login_required
def users_followers(user_id):
    return render_template(
        'users/followers.html', user=User.query.get(user_id))


@app.route('/users/<int:user_id>', methods=["GET"])
def users_show(user_id):
    found_user = User.query.get(user_id)
    return render_template('users/show.html', user=found_user)


@app.route('/users/<int:user_id>/edit')
@login_required
@ensure_correct_user
def users_edit(user_id):
    found_user = User.query.get(user_id)
    return render_template(
        'users/edit.html',
        form=UserForm(obj=found_user),
        user_id=found_user.id)


@app.route('/users/<int:user_id>', methods=["PATCH"])
@login_required
@ensure_correct_user
def users_update(user_id):
    found_user = User.query.get(user_id)
    form = UserForm(request.form)
    if form.validate():
        if User.authenticate(found_user.username, form.password.data):
            found_user.username = form.username.data
            found_user.email = form.email.data
            found_user.image_url = form.image_url.data or "/static/images/default-pic.png"
            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('users_show', user_id=user_id))
        flash({
            'text': "Wrong password, please try again.",
            'status': 'danger'
        })
    return render_template('users/edit.html', form=form, user_id=found_user.id)


@app.route('/users/<int:user_id>', methods=["DELETE"])
@login_required
@ensure_correct_user
def users_destroy(user_id):
    found_user = User.query.get(user_id)
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for('users_new'))


# Messages routes
@app.route('/users/<int:user_id>/messages', methods=["POST"])
@login_required
@ensure_correct_user
def messages_index(user_id):
    form = MessageForm()
    if form.validate():
        new_message = Message(text=form.text.data, user_id=user_id)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('users_show', user_id=user_id))
    return render_template('messages/new.html', form=form)


@app.route('/users/<int:user_id>/messages/new')
@login_required
@ensure_correct_user
def messages_new(user_id):
    return render_template('messages/new.html', form=MessageForm())


@app.route('/users/<int:user_id>/messages/<int:message_id>', methods=["GET"])
def messages_show(user_id, message_id):
    found_message = Message.query.get(message_id)
    return render_template('messages/show.html', message=found_message)


@app.route(
    '/users/<int:user_id>/messages/<int:message_id>', methods=["DELETE"])
@login_required
@ensure_correct_user
def messages_destroy(user_id, message_id):
    found_message = Message.query.get(message_id)
    db.session.delete(found_message)
    db.session.commit()
    return redirect(url_for('users_show', user_id=user_id))


@app.route('/')
def root():
    messages = []
    if current_user.is_authenticated:
        messages = Message.query.order_by(
            Message.timestamp.desc()).limit(100).all()
    return render_template('home.html', messages=messages)


# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
