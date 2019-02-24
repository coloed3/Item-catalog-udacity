from _functools import wraps
from flask import redirect
from flask import session as login_session

# https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
# above explains the why for the wraps when logging
def required_login(f):
    @wraps(f)
    def x(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return x