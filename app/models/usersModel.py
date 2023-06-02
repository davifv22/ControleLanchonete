from app import db, UserMixin

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(10))
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(200))
    administrador = db.Column(db.String(20))
    situacao = db.Column(db.String(20))
    dt_criacao = db.Column(db.String(50))
    
    def __init__(self, user, nome, email, senha, administrador, situacao, dt_criacao):
        self.user = user
        self.nome = nome
        self.email = email
        self.senha = senha
        self.administrador = administrador
        self.situacao = situacao
        self.dt_criacao = dt_criacao
    
    def get_user(user):
        return users.query.get(user)