from functools import wraps

from pengar.www.util import get_current_user
from flask import abort

def login_required(controller):
    @wraps(controller)
    def wrapper(*args, **kw):
        user = get_current_user()
        if not user:
            return abort(403)

        return controller(*args, **kw)
    return wrapper
