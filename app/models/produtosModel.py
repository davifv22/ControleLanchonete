from app import db, UserMixin

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