from flask import Flask, Blueprint, redirect, render_template, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import secrets
import locale


# CRIA E CONFIGURA APP
app = Flask(__name__)
app.config.from_object('config')

# CRIA DB E LOGIN
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def get(user):
    return usersModel.users.get_user(user)


# DEFINE LOCALIDADE DA MOEDA
locale.setlocale(locale.LC_ALL, '')

# IMPORTA OS MODELS
from .models import controleModel, empresaModel, pedidosModel, produtosModel, usersModel

# IMPORTA OS SERVICES
from .services import auth, create_db, load, order, product, uploads
app.register_blueprint(auth.bp)

# CRIA OS ROTEAMENTOS
from .views import index, cad, panel
app.register_blueprint(index.bp)
app.register_blueprint(cad.bp)
app.register_blueprint(panel.bp)
app.add_url_rule('/', endpoint='index')
login_manager.login_view = "index.index_"
