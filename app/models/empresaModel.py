from app import db, UserMixin

class empresa(UserMixin, db.Model):
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
    dt_criacao = db.Column(db.String(50))
    
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