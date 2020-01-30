import json
from flask import url_for

def test_ping(client):
    rv = client.get(url_for('ping'))
    assert rv.status_code == 200
