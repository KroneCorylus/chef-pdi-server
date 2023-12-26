from flask import Response, jsonify, make_response


def flask_error_handler(code: int, message: str) -> Response:
    error_message = {'error': str(message)}
    response = make_response(jsonify(error_message), code)
    response.headers['Content-Type'] = 'application/json'
    return response
