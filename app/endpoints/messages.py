from collections import OrderedDict
from flask import Blueprint, jsonify, request, make_response, json
from ..models import Message
from ..security import validate_input, validate_content, token_required
from app import db
from sqlalchemy import and_
import datetime
from http import HTTPStatus

messages_blueprint = Blueprint('messages', __name__, url_prefix='/messages')


# given token, sender id, recipient id, and message content, sends messages to recipient
@messages_blueprint.route('', methods=['post'])
@token_required
@validate_input([('sender', int), ('recipient', int), ('content', dict)])
def create_messages(outgoing_message, uid):
    # check if sender is the id specified in token
    if uid != outgoing_message['sender']:
        return make_response(jsonify({"message": "Unauthorized User"}), HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Bearer realm="Login required"'})

    error_message = validate_content(outgoing_message['content'])
    if error_message is not None:
        return make_response(jsonify({"message": error_message}), HTTPStatus.BAD_REQUEST)

    # encode message content dict to json and store in msg column, add datetime of message
    timestamp = datetime.datetime.utcnow()
    new_message = Message(timestamp=timestamp, sender=outgoing_message['sender'],
                          recipient=outgoing_message['recipient'], content=json.dumps(outgoing_message['content']))

    if not new_message:
        return make_response(jsonify({"message": "Message creation failed"}), HTTPStatus.INTERNAL_SERVER_ERROR)

    db.session.add(new_message)
    db.session.commit()

    # return unique message id auto-incremented at each insertion
    return make_response(jsonify({'id': new_message.id, 'timestamp': timestamp}), HTTPStatus.OK)


# given recipient id, start, and limit, return limit messages for recipient from msg start
@messages_blueprint.route('', methods=['get'])
@token_required
@validate_input([('recipient', int), ('start', int), ('limit', int)])
def get_messages(params, uid):
    if uid != params['recipient']:
        return make_response(jsonify({"message": "Unauthorized User"}), HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Bearer realm="Login required"'})

    start = params['start']
    recipient = params['recipient']
    limit = params['limit']

    # parameterized query with int as inputs reduces risk of SQL injection
    messages = Message.query.filter(and_(Message.id >= start,
                                         Message.recipient == recipient)).limit(limit).all()

    # messages and output contain repeat info, need to optimize for better space complexity
    output = []
    for message in messages:
        output.append(OrderedDict([("id", message.id),
                                   ("timestamp", message.timestamp),
                                   ("sender", message.sender),
                                   ("recipient", message.recipient),
                                   ("content", eval(message.content))]))

    return make_response(jsonify({"messages": output}), HTTPStatus.OK)
