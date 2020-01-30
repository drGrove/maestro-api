from flask import current_app as app
from flask import jsonify
from flask import make_response
from flask import request

from .. import db
from ..models.repositories import Repository


@app.route('/repository', methods=['POST'])
def create_repository():
    body = request.get_json()
    if body is None:
        return make_response(jsonify({
            "error": True,
            "msg": "Invalid input data, must be json"
        }), 400)
    body_error = False
    body_error_messages = []
    if body.get('name') is None or body.get('name') == "":
        body_error = True
        body_error_messages.append('Missing name')
    if body.get('url') is None or body.get('url') == "":
        body_error = True
        body_error_messages.append('Missing URL')
    if body_error:
        return make_response(jsonify({
            "error": True,
            "err_msg_type": "array",
            "msg": body_error_messages
        }), 400)

    repository = Repository(
        name=body['name'],
        url=body['url']
    )
    db.session.add(repository)
    db.session.commit()
    return make_response(jsonify(repository.to_dict()), 201)
