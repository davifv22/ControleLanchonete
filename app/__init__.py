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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# CONFIGURAÇÃO PARA UPLOADS
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'app/static/img')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# DEFINE LOCALIDADE DA MOEDA
locale.setlocale(locale.LC_ALL, '')

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
    situation = db.Column(db.String(50))
    
    def __init__(self, user, name, email, password, dt_create, situation):
        self.user = user
        self.name = name
        self.email = email
        self.password = password
        self.dt_create = dt_create
        self.situation = situation

class pedidos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_client = db.Column(db.String(100))
    payment = db.Column(db.String(100))
    delivery = db.Column(db.String(100))
    note = db.Column(db.String(200))
    amount = db.Column(db.String(100))
    address = db.Column(db.String(100))
    tel = db.Column(db.String(200))
    order_time = db.Column(db.String(200))
    order_start = db.Column(db.String(200))
    situation = db.Column(db.String(50))
    
    def __init__(self, name_client, payment, delivery, note, amount, address, tel, order_time, order_start, situation):
        self.name_client = name_client
        self.payment = payment
        self.delivery = delivery
        self.note = note
        self.amount = amount
        self.address = address
        self.tel = tel
        self.order_time = order_time
        self.order_start = order_start
        self.situation = situation
        
class pedidos_items(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer)
    product_name = db.Column(db.String(100))
    additional = db.Column(db.String(100))
    note = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    situation = db.Column(db.String(50))
    
    def __init__(self, id_pedido, product_name, additional, note, amount, situation):
        self.id_pedido = id_pedido
        self.product_name = product_name
        self.additional = additional
        self.note = note
        self.amount = amount
        self.situation = situation

class cadempresa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100))
    corporate_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    district = db.Column(db.String(200))
    city = db.Column(db.String(200))
    cep = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tel = db.Column(db.String(50))
    cnpj = db.Column(db.String(50))
    dt_create = db.Column(db.DATETIME)
    
    def __init__(self, company_name, corporate_name, address, district, city, cep, email, tel, cnpj, dt_create):
        self.company_name = company_name
        self.corporate_name = corporate_name
        self.address = address
        self.district = district
        self.city = city
        self.cep = cep
        self.email = email
        self.tel = tel
        self.cnpj = cnpj
        self.dt_create = dt_create

class produtos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    amount = db.Column(db.String(50))
    description = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    situation = db.Column(db.String(50))
    
    def __init__(self, title, amount, description, picture, situation):
        self.title = title
        self.amount = amount
        self.description = description
        self.picture = picture
        self.situation = situation

    
class adicionais(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    amount = db.Column(db.String(50))
    situation = db.Column(db.String(50))
    
    def __init__(self, title, amount, situation):
        self.title = title
        self.amount = amount
        self.situation = situation
        

class controle(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    debito = db.Column(db.String(50))
    dt_ref = db.Column(db.String(50))
    
    def __init__(self, debito, dt_ref):
        self.debito = debito
        self.dt_ref = dt_ref


# FUNÇÕES GLOBAIS
def load_menu():
    empresa = cadempresa.query.filter_by(id=1).first()
    if empresa is None:
        company_name = 'NOME EMPRESA'
    else:
        company_name = empresa.company_name
    username = current_user.name
    badgeOrder = pedidos.query.filter_by(situation='PENDENTE').all()
    return username, company_name, len(badgeOrder)


def load_values_panel():
    # debito
    debito = db.session.query(db.func.sum(controle.debito)).scalar()
    
    if db.session.query(db.func.sum(pedidos.amount)).filter(pedidos.situation == 'FINALIZADO').scalar() is None:
        faturamento = 0
    else:
        faturamento = db.session.query(
            db.func.sum(pedidos.amount)).filter(pedidos.situation == 'FINALIZADO').scalar()
        
    # if db.session.query(db.func.sum(compras.valor_total)).scalar() is None:
    despesas = -875.00
    # else:
    #     despesas = db.session.query(db.func.sum(compras.valor_total)).scalar()
    total = float(debito) + float(faturamento) + float(despesas)
    return locale.currency(debito, grouping=True), locale.currency(faturamento, grouping=True), locale.currency(despesas, grouping=True), locale.currency(total, grouping=True)

def upload_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return False

# CRIA OS ROTEAMENTOS
from . import index
app.register_blueprint(index.bp)
app.add_url_rule('/', endpoint='index')

from . import auth
app.register_blueprint(auth.bp)

from . import panel
app.register_blueprint(panel.bp)

from . import cad
app.register_blueprint(cad.bp)