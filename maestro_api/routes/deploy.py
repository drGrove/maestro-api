from datetime import datetime
from flask import current_app as app
from flask import jsonify
from flask import make_response
from flask import request

from .. import db
from ..models.deploy import Deploy, DeployStatus


@app.route('/deploy', methods=['POST'])
def create_deployment():
    body = request.get_json()
    if body is None:
        return make_response(jsonify({
            "msg": "Invalid input data, must be json"
        }), 400)
    body_error = False
    body_error_messages = []
    if body.get('build_number') is None or body.get('build_number') == "":
        body_error = True
        body_error_messages.append("Missing build_number")
    if body.get('repo_id') is None or body.get('repo_id') == "":
        body_error = True
        body_error_messages.append("Missing repo identifier")
    if body.get('config') is None or body.get('config') == "":
        body_error = True
        body_error_messages.append('Missing configuration for deployment')
    if body.get('env') is None or body.get('env') == "":
        body_error = True
        body_error_messages.append('Missing env for deployment')
    if body_error:
        return make_response(jsonify({
            "error": True,
            "err_msg_type": "array",
            "msg": body_error_messages
        }), 400)

    deploy = Deploy(
        build_number=body['build_number'],
        repo_id=body['repo_id'],
        config=body['config'],
        env=body['env'],
        status=DeployStatus.PENDING
    )
    db.session.add(deploy)
    db.session.commit()
    return make_response(jsonify(deploy.to_dict()), 201)

@app.route('/deploy', methods=['GET'])
def list_deployments():
    deployments = Deploy.query.all()
    return make_response(jsonify([deploy.to_dict() for deploy in deployments]), 200)

@app.route('/deploy/<id>', methods=['GET'])
def get_deployment(id):
    deploy = Deploy.query.get(id)
    if deploy is None:
        return make_response(jsonify({}), 404)
    return make_response(jsonify(deploy.to_dict()), 200)

@app.route('/deploy/<id>', methods=['PUT'])
def update_deployment(id):
    body = request.get_json()
    deploy = Deploy.query.get(id)
    if body['completed']:
        deploy.completed = datetime.fromtimestamp(body['completed'])
    if body['status']:
        deploy.status = DeployStatus(body['status'])
    db.session.commit()
    return make_response(jsonify(deploy.to_dict()), 200)
