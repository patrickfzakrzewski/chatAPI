import datetime
import jwt
from flask import Blueprint, jsonify, make_response
from werkzeug.security import check_password_hash
from ..models import User
from ..security import validate_input
import app
from http import HTTPStatus

# minimum expiry time for token
DEFAULT_EXP_MINUTES = 30
MAX_CREDENTIAL_LENGTH = 50

login_blueprint = Blueprint('login', __name__, url_prefix='/login')


@login_blueprint.route('', methods=['post'])
@validate_input([('username', str), ('password', str)])
def login(credentials):
    username = credentials['username']
    password = credentials['password']
    curUser = User.query.filter_by(username=username).first()

    # check if user exists and if password is correct
    if not curUser or not check_password_hash(curUser.password, password):
        return make_response(jsonify({"message": 'Could not verify'}), HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Basic realm="Login required"'})

    # return jwt as bearer token, set default expiration time to 30 min
    token = jwt.encode({'uid': curUser.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=DEFAULT_EXP_MINUTES)},
                       app.config.Config.SECRET_KEY, algorithm='HS256')
    if not token:
        return make_response(jsonify({"message": "Token creation failed"}), HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({'id': curUser.id, 'token': token}, HTTPStatus.OK)

