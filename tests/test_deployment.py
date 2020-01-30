import json
import pytest
from datetime import datetime

from flask import url_for

from .utils import create_deployment
from .utils import create_repository

def test_create_deployment(client):
	repo_data = {
		"name": "BitGo/test",
		"url": "https://github.com/test/test"
	}
	repo_rv = create_repository(client, repo_data)
	repo_rv_dict = json.loads(repo_rv.data)
	data = {
		"build_number": 1,
		"repo_id": repo_rv_dict['id'],
		"config": "Some config",
		"env": "dev",
	}
	deployment_rv = create_deployment(client, data)
	assert deployment_rv.status_code == 201
	deployment_json = deployment_rv.json
	assert deployment_json['status'] == 'pending'

def test_list_deployments(client):
	deployments_rv = client.get(url_for('list_deployments'))
	assert len(deployments_rv.json) == 1

def test_get_deployment(client):
    deployment_rv = client.get(url_for('get_deployment', id=1))
    deployment_json = deployment_rv.json
    assert deployment_json['id'] == 1
    assert deployment_json['status'] == "pending"

def test_update_deployment(client):
    deployment_rv = client.put(
        url_for('update_deployment', id=1),
        data=json.dumps(dict(
            status="completed",
            completed=datetime.timestamp(datetime.now())
        )),
        content_type="application/json"
    )
    assert deployment_rv.status_code == 200

def test_get_missing_deployment(client):
    deployment_rv = client.get(url_for('get_deployment', id=1000000000))
    assert deployment_rv.status_code == 404

def test_create_deployment_missing_data(client):
    deployment_rv = client.post(
        url_for('create_deployment'),
        data=json.dumps({}),
        content_type="application/json"
    )
    assert deployment_rv.status_code == 400
    deployment_json = deployment_rv.json
    assert deployment_json['error'] == True
    assert deployment_json['err_msg_type'] == "array"
    assert 'Missing env for deployment' in deployment_json['msg']
    assert 'Missing build_number' in deployment_json['msg']
    assert 'Missing repo identifier' in deployment_json['msg']
    assert 'Missing configuration for deployment' in deployment_json['msg']

def test_create_deployment_no_body(client):
    deployment_rv = client.post(url_for('create_deployment'))
    assert deployment_rv.status_code == 400
