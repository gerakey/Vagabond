from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_cors import CORS
from config import VAGABOND_CONFIG

app = Flask(__name__, static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{VAGABOND_CONFIG['mysql_user']}:{VAGABOND_CONFIG['mysql_password']}@{VAGABOND_CONFIG['mysql_server']}:{VAGABOND_CONFIG['mysql_port']}/{VAGABOND_CONFIG['mysql_database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'v5t8IIbv7c8xw59sqoQInUHEouXqVLSHrvw0Ggk00_BiBNSBXH--qU_tiwGER8uf_-vsOdh6Pjwf2vYL1I_U7-rdFYvZ-C2C6sYokT6HGww-WaH97BGrRKHcUmt0kFb-sJRfAFik5-QPERSXEdmCya4uvRRVxX8bI2126dbM20A'

db = SQLAlchemy(app)
limiter = Limiter(app)
cors = CORS(app)

from routes import *

if __name__ == '__main__':
    app.run()
