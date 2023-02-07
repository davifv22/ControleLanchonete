from app import *


def prepare(id):
    situation = "EM ANDAMENTO"
    order_start = datetime.now().strftime('%d-%m-%H %H:%M:%S')
    pedidos.query.filter_by(id=id).update(
        {"order_start": order_start, "situation": situation})
    return True


def deliver(id):
    delivery = pedidos.query.filter_by(id=id).first()
    if delivery.delivery == 'ENTREGA':
        situation = "EM ENTREGA"
        pedidos.query.filter_by(id=id).update(
            {"situation": situation})
    else:
        situation = "RETIRAR"
        pedidos.query.filter_by(id=id).update(
            {"situation": situation})
    return True


def finalize(id):
    situation = "FINALIZADO"
    pedidos.query.filter_by(id=id).update(
        {"situation": situation})
    return True


def cancel(id):
    situation = "CANCELADO"
    pedidos.query.filter_by(id=id).update(
        {"situation": situation})
    return True

def update(id):
    name_client = request.form['name_client']
    payment = request.form['payment']
    address = request.form['address']
    delivery = request.form['delivery']
    tel = request.form['tel']
    note = request.form['note']
    pedidos.query.filter_by(id=id).update(
    {"name_client": name_client, "payment": payment, "address": address, "delivery": delivery, "tel": tel, "note": note})
    return True