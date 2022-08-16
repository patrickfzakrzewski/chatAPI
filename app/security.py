# defines several functions/classes to be used in input and token validation
from flask import request, make_response, jsonify
from http import HTTPStatus
import jwt
from functools import wraps
import app

# defines minimum acceptable input size from requests
MIN_CREDENTIAL_SIZE = 1
MAX_CREDENTIAL_SIZE = 50
MIN_NUMERICAL_INPUT = 0
MAX_NUMERICAL_INPUT = 10000


# class to be used in input validation and to return error messages for missing/incorrect parameters
class SchemaValidator():
    def __init__(self, fields=[], response={}):
        self.fields = fields
        self.response = response

    def isTrue(self):
        errorMessages: list[str] = []
        for field in self.fields:
            try:
                parameter = self.response.get(field[0], None)
                if parameter is None or type(parameter) != field[1]:
                    raise Exception("Error: missing {} parameter".format(field[0]))

                elif type(parameter) == str:
                    if len(parameter) < MIN_CREDENTIAL_SIZE:
                        raise Exception("Error: {} must be at least length {}".format(field[0], MIN_CREDENTIAL_SIZE))
                    if len(parameter) > MAX_CREDENTIAL_SIZE:
                        raise Exception("Error: {} must be at most length {}".format(field[0], MAX_CREDENTIAL_SIZE))

                elif type(parameter) == int:
                    if parameter < MIN_NUMERICAL_INPUT:
                        raise Exception("Error: {} must be at least {}".format(field[0], MIN_NUMERICAL_INPUT))
                    if parameter > MAX_NUMERICAL_INPUT:
                        raise Exception("Error: {} must be at most {}".format(field[0], MAX_NUMERICAL_INPUT))

            except Exception as e:
                errorMessages.append(str(e))
        return errorMessages


# wrapper function to validate inputs according to the designated fields and types
def validate_input(fields):
    def wrap(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            input = request.get_json()
            _instance = SchemaValidator(fields=fields, response=input)
            response = _instance.isTrue()

            if len(response) > 0:
                return make_response(jsonify({"message": response}), HTTPStatus.BAD_REQUEST)

            return f(input, *args, **kwargs)

        return decorated

    return wrap


# helper function to validate content of messages sent
def validate_content(content):
    msgtype = content.get('type')
    if msgtype is None or type(msgtype) is not str or msgtype not in ['text', 'image', 'video']:
        return "Invalid Message Type"

    elif msgtype == 'text':
        text = content.get('text')
        if text is None or type(text) is not str:
            return "Invalid Text Message"

    elif msgtype == 'image':
        URI = content.get('url')
        height = content.get('height')
        width = content.get('width')
        if URI is None or height is None or width is None:
            return "Missing Image Parameter"
        elif type(URI) is not str or type(height) is not int or type(width) is not int:
            return "Invalid Image Parameter"

    elif msgtype == 'video':
        URI = content.get('url')
        source = content.get('source')
        if URI is None or source is None:
            return "Missing Video Parameter"
        elif type(URI) is not str or type(source) is not str or source not in ['youtube', 'vimeo']:
            return "Invalid Video Parameter"


# decorated function to determine whether bearer token is valid, passes decrypted uid
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers.get('Authorization').split()

        auth_type = headers[0]
        token = headers[1]

        if auth_type != 'Bearer':
            return make_response(jsonify({'message': 'Required Bearer Authorization'}), HTTPStatus.UNAUTHORIZED,
                                 {'WWW-Authenticate': 'Bearer realm="Login required"'})
        if not token:
            return make_response(jsonify({'message': 'Token is missing!'}), HTTPStatus.UNAUTHORIZED,
                                 {'WWW-Authenticate': 'Bearer realm="Login required"'})
        try:
            data = jwt.decode(token, app.config.Config.SECRET_KEY, algorithms='HS256')
        except:
            return make_response(jsonify({'message': 'Token is invalid'}), HTTPStatus.UNAUTHORIZED,
                                 {'WWW-Authenticate': 'Bearer realm="Login required"'})

        return f(data['uid'], *args, **kwargs)

    return decorated

