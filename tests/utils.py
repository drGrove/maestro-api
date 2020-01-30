import json
import unittest

from flask import url_for

def create_deployment(c, data):
    return c.post(url_for('create_deployment'), data=json.dumps(data), content_type='application/json')

def create_repository(c, data):
    return c.post(url_for('create_repository'), data=json.dumps(data), content_type='application/json')
