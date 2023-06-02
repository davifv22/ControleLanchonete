from app import empresaModel, pedidosModel, current_user, db, locale, controleModel

class menu():
    def get():
        empresa = empresaModel.empresa.query.filter_by(id=1).first()
        if empresa is None:
            nome_empresa = 'NOME EMPRESA'
        else:
            nome_empresa = empresa.nome_empresa
        nome = current_user.nome
        badgeOrder = pedidosModel.pedidos.query.filter_by(situacao='PENDENTE').all()
        return nome, nome_empresa, len(badgeOrder)
    
    
class values_panel():
    def get():
        debito = db.session.query(db.func.sum(controleModel.controle.debito)).scalar()
        if debito is None:
            debito = 0
        
        faturamento = db.session.query(db.func.sum(pedidosModel.pedidos.total)).filter(pedidosModel.pedidos.situacao == 'FINALIZADO').scalar()
        if faturamento is None:
            faturamento = 0
            
            
        # if db.session.query(db.func.sum(compras.valor_total)).scalar() is None:
        despesas = -875.00
        # else:
        #     despesas = db.session.query(db.func.sum(compras.valor_total)).scalar()
        total = float(debito) + float(faturamento) + float(despesas)
        return locale.currency(debito, grouping=True), locale.currency(faturamento, grouping=True), locale.currency(despesas, grouping=True), locale.currency(total, grouping=True)
    
class menu_index():
    def get():
        empresa = empresaModel.empresa.query.filter_by(id=1).first()
        if empresa is None:
            nome_empresa = 'NOME EMPRESA'
        else:
            nome_empresa = empresa.nome_empresa
        return nome_empresa