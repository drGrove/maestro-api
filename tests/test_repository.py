import json
import pytest
from datetime import datetime

from flask import url_for

from .utils import create_repository

def test_create_repository(client):
    repo_data = {
		"name": "test/test",
		"url": "https://github.com/test/test"
	}
    repo_rv = create_repository(client, repo_data)
    assert repo_rv.status_code == 201
    repo_rv_dict = repo_rv.json
    assert repo_rv_dict.get('name') == 'test/test'
    assert repo_rv_dict.get('id') == 2
    assert repo_rv_dict.get('url') == "https://github.com/test/test"

def test_create_repository_no_body(client):
    repo_rv = create_repository(client, None)
    assert repo_rv.status_code == 400

def test_create_repository_missing_data(client):
    repo_rv = client.post(
        url_for('create_repository'),
        data=json.dumps({}),
        content_type="application/json"
    )
    assert repo_rv.status_code == 400
    assert repo_rv.json.get('error') == True
    assert repo_rv.json.get('err_msg_type') == "array"
    assert 'Missing name' in repo_rv.json.get('msg')
    assert 'Missing URL' in repo_rv.json.get('msg')
