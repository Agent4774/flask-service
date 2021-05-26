from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'some_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db')
db = SQLAlchemy(app)
logging.basicConfig(
	filename='service/logs/service.log', 
	level=logging.INFO,
	format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)


from service import routes, models