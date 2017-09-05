from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
port = int(os.getenv("VCAP_APP_PORT"))

from app import views, models, forms
