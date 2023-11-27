from functools import wraps
from flask_login import current_user
from flask import render_template


def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'superuser':
            message = 'You do not have the necessary permissions to access this page.'
            return render_template('dashboard.html', message=message)
        return f(*args, **kwargs)
    return decorated_function
