from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps


def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('user_id') != current_user.id:
            flash({'text': "Not Authorized", 'status': 'danger'})
            return redirect(url_for('root'))
        return fn(*args, **kwargs)

    return wrapper
