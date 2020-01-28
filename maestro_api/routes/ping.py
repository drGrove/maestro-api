from datetime import datetime

from flask import current_app as app
from flask import jsonify
from flask import make_response


@app.route('/')
def ping():
    return make_response(jsonify({
        "timestamp": datetime.timestamp(datetime.now())
    }), 200)
