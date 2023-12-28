from functools import wraps
import jwt
from flask import make_response, request
from flask import current_app
from ..config import SECRET_KEY
import re


def token_required(role: str | None = None):

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            if SECRET_KEY is None:
                return f(*args, **kwargs)

            token = request.headers.get('Authorization')

            if not token:
                return make_response('Invalid credentials', 401)

            # Clear token prefix
            token = re.sub(r"^.*?\s", "", token)

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                print(SECRET_KEY, data)
            except Exception as err:
                print(err)
                return make_response('Invalid credentials', 401)

            if role is not None:
                if data.get('role') is None:
                    return make_response('Invalid role', 403)
                if role != data['role']:
                    return make_response('Invalid role', 403)

            return f(*args, **kwargs)
        return decorated

    return decorator
