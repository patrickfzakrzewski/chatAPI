import http.client
from typing import List

from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..security import validate_input
from app import db
from http import HTTPStatus

user_blueprint = Blueprint('user', __name__, url_prefix='/users')


# register users by username and password, return unique user id
@user_blueprint.route('', methods=['post'])
@validate_input([('username', str), ('password', str)])
def register(credentials):
    username = credentials['username']
    password = credentials['password']

    # always 64 chars long
    hashed_password = generate_password_hash(password, method='sha256')

    # sql_alchemy utilizes parameterized queries to reduce risk of SQL injection
    if User.query.filter_by(username=username).first() is not None:
        return make_response(jsonify({"message": "Username is taken"}), HTTPStatus.CONFLICT)

    new_user = User(username=username, password=hashed_password)

    if not new_user:
        return make_response(jsonify({"message": "User creation failed"}), HTTPStatus.INTERNAL_SERVER_ERROR)

    # should also add verification that db add/commit was successful
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({"id": new_user.id}), HTTPStatus.OK)
