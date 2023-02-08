from app import *


def prepare(id):
    situacao = "EM ANDAMENTO"
    dt_incio = datetime.now().strftime('%d-%m-%H %H:%M:%S')
    pedidos.query.filter_by(id=id).update(
        {"dt_incio": dt_incio, "situacao": situacao})
    return True


def deliver(id):
    delivery = pedidos.query.filter_by(id=id).first()
    if delivery.delivery == 'ENTREGA':
        situacao = "EM ENTREGA"
        pedidos.query.filter_by(id=id).update(
            {"situacao": situacao})
    else:
        situacao = "RETIRAR"
        pedidos.query.filter_by(id=id).update(
            {"situacao": situacao})
    return True


def finalize(id):
    situacao = "FINALIZADO"
    pedidos.query.filter_by(id=id).update(
        {"situacao": situacao})
    return True


def cancel(id):
    situacao = "CANCELADO"
    pedidos.query.filter_by(id=id).update(
        {"situacao": situacao})
    return True

def update(id):
    nome_cliente = request.form['nome_cliente']
    pagamento = request.form['pagamento']
    endereco = request.form['endereco']
    tipo_entrega = request.form['delivery']
    tel = request.form['tel']
    observacao = request.form['note']
    pedidos.query.filter_by(id=id).update(
    {"nome_cliente": nome_cliente, "pagamento": pagamento, "endereco": endereco, "tipo_entrega": tipo_entrega, "tel": tel, "observacao": observacao})
    return True