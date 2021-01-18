from vagabond.__main__ import app

@app.errorhandler(404)
def route_error_404(e):
    return app.send_static_file('index.html')

@app.route('/')
def index():
    return app.send_static_file('index.html')
