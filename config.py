from flask import Flask
from flask_login import LoginManager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

DB_NAME = 'datas.db'
ADMIN_USER_NAME = 'admin'
ADMIN_PASSWORD = '1234'
ADMIN_NAME = 'Mehmet'
ADMIN_SURNAME = 'Akay'

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['JSON_AS_ASCII'] = False

AppRoot = os.path.dirname(os.path.abspath(__file__))
DbFilePath = AppRoot + '/static/data/' + DB_NAME
DbPath = 'sqlite:///' + DbFilePath
engine = create_engine(DbPath, convert_unicode=True, connect_args={'check_same_thread': False}, echo=False)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()