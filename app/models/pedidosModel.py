from app import db, UserMixin

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