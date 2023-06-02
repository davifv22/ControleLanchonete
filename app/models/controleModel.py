from app import db, UserMixin

class controle(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    debito = db.Column(db.String(50))
    dt_ref = db.Column(db.String(50))
    
    def __init__(self, debito, dt_ref):
        self.debito = debito
        self.dt_ref = dt_ref