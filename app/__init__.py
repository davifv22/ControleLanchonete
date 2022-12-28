from flask import Flask, Blueprint, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from datetime import datetime
import secrets

# CRIA E CONFIGURA APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# CRIA DB E LOGIN
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
from . import create_db

# VALIDAÇÃO USER LOGADO
@login_manager.user_loader
def get(user):
    return users.query.get(user)

# CRIA OS BANCOS
class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(10))
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    dt_create = db.Column(db.DATETIME)
    situacao = db.Column(db.String(1))
    
    def __init__(self, user, name, email, password, dt_create, situacao):
        self.user = user
        self.name = name
        self.email = email
        self.password = password
        self.dt_create = dt_create
        self.situacao = situacao

# CRIA OS ROTEAMENTOS
from . import index
app.register_blueprint(index.bp)
app.add_url_rule('/', endpoint='index')

from . import auth
app.register_blueprint(auth.bp)

from . import panel
app.register_blueprint(panel.bp)