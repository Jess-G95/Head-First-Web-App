from flask import session, redirect, url_for, flash
from functools import wraps

def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        flash('Please log in to view the log.')
        return redirect(url_for('do_login')) 
    return wrapper
