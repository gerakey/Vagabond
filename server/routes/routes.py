from flask import make_response

from __main__ import app

@app.route('/')
def index():
    return make_response('Hello, world!', 200)
