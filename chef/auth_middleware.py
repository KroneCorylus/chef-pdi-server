from functools import wraps
import jwt
from flask import make_response, request
from flask import current_app


def token_required(rol):
    print(rol)

    def decorator(f):
        print('magia')

        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return make_response('Invalid credentials', 401)

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'])
            except:
                return make_response('Invalid credentials', 401)

            if rol != data['rol']:
                return make_response('Invalid role', 403)

            return f(*args, **kwargs)
        return decorated

    return decorator
