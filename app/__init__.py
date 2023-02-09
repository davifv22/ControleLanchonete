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
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(200))
    administrador = db.Column(db.String(20))
    situacao = db.Column(db.String(20))
    dt_criacao = db.Column(db.DATETIME)
    
    def __init__(self, user, nome, email, senha, administrador, situacao, dt_criacao):
        self.user = user
        self.nome = nome
        self.email = email
        self.senha = senha
        self.administrador = administrador
        self.situacao = situacao
        self.dt_criacao = dt_criacao


class controle(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    debito = db.Column(db.String(50))
    dt_ref = db.Column(db.String(50))
    
    def __init__(self, debito, dt_ref):
        self.debito = debito
        self.dt_ref = dt_ref


class cadempresa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_empresa = db.Column(db.String(100))
    razao_social = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    bairro = db.Column(db.String(200))
    cidade = db.Column(db.String(50))
    cep = db.Column(db.String(20))
    email = db.Column(db.String(50))
    tel = db.Column(db.String(20))
    cnpj = db.Column(db.String(20))
    dt_criacao = db.Column(db.DATETIME)
    
    def __init__(self, nome_empresa, razao_social, endereco, bairro, cidade, cep, email, tel, cnpj, dt_criacao):
        self.nome_empresa = nome_empresa
        self.razao_social = razao_social
        self.endereco = endereco
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.email = email
        self.tel = tel
        self.cnpj = cnpj
        self.dt_criacao = dt_criacao


class produtos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100))
    valor_custo = db.Column(db.String(20))
    valor_venda = db.Column(db.String(20))
    descricao = db.Column(db.String(400))
    foto = db.Column(db.String(50))
    itens = db.Column(db.String(50))
    situacao = db.Column(db.String(10))
    
    
    def __init__(self, titulo, valor_custo, valor_venda, descricao, foto, itens, situacao):
        self.titulo = titulo
        self.valor_custo = valor_custo
        self.valor_venda = valor_venda
        self.descricao = descricao
        self.foto = foto
        self.itens = itens
        self.situacao = situacao
        
class produtos_itens(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100))
    tipo_item = db.Column(db.String(30))
    valor_custo = db.Column(db.String(20))
    valor_venda = db.Column(db.String(20))
    situacao = db.Column(db.String(20))
    
    def __init__(self, titulo, tipo_item, valor_custo, valor_venda, situacao):
        self.titulo = titulo
        self.tipo_item = tipo_item
        self.valor_custo = valor_custo
        self.valor_venda = valor_venda
        self.situacao = situacao
        
class pedidos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100))
    sub_total = db.Column(db.String(100))
    tipo_entrega = db.Column(db.String(100))
    total = db.Column(db.String(200))
    total_itens = db.Column(db.String(100))
    observacao = db.Column(db.String(200))
    pagamento = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    tel = db.Column(db.String(200))
    dt_pedido = db.Column(db.String(50))
    dt_inicio = db.Column(db.String(50))
    dt_concluido = db.Column(db.String(50))
    situacao = db.Column(db.String(50))
    
    def __init__(self, nome_cliente, sub_total, tipo_entrega, total, total_itens, observacao, pagamento, endereco, tel, dt_pedido, dt_inicio, dt_concluido, situacao):
        self.nome_cliente = nome_cliente
        self.sub_total = sub_total
        self.tipo_entrega = tipo_entrega
        self.total = total
        self.total_itens = total_itens
        self.observacao = observacao
        self.pagamento = pagamento
        self.endereco = endereco
        self.tel = tel
        self.dt_pedido = dt_pedido
        self.dt_inicio = dt_inicio
        self.dt_concluido = dt_concluido
        self.situacao = situacao
        
class pedidos_itens(UserMixin, db.Model):
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer)
    nome_item = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    valor = db.Column(db.String(100))
    observacao = db.Column(db.String(100))
    situacao = db.Column(db.String(50))
    
    def __init__(self, id_pedido, product_name, additional, note, amount, situacao):
        self.id_pedido = id_pedido
        self.product_name = product_name
        self.additional = additional
        self.note = note
        self.amount = amount
        self.situacao = situacao


# FUNÇÕES GLOBAIS
def load_menu():
    empresa = cadempresa.query.filter_by(id=1).first()
    if empresa is None:
        nome_empresa = 'NOME EMPRESA'
    else:
        nome_empresa = empresa.nome_empresa
    nome = current_user.nome
    badgeOrder = pedidos.query.filter_by(situacao='PENDENTE').all()
    return nome, nome_empresa, len(badgeOrder)


def load_values_panel():
    # debito
    if db.session.query(db.func.sum(controle.debito)).scalar() is None:
        debito = 0
    
    if db.session.query(db.func.sum(pedidos.total)).filter(pedidos.situacao == 'FINALIZADO').scalar() is None:
        faturamento = 0
    else:
        faturamento = db.session.query(
            db.func.sum(pedidos.total)).filter(pedidos.situacao == 'FINALIZADO').scalar()
        
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