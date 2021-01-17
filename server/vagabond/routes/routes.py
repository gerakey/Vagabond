from flask import make_response

from vagabond.__main__ import app

@app.route('/')
def index():
    return make_response('Hello, world!', 200)
