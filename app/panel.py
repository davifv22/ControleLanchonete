from app import *

bp = Blueprint('panel', __name__, url_prefix='/painel')


@bp.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass

    menu_panel = load_menu()
    values_panel = load_values_panel()
    return render_template('panel/home.html', menu_panel=menu_panel, values_panel=values_panel)


@bp.route('/pedido/<int:id>', methods=['POST', 'GET'])
@bp.route('/pedidos', methods=['POST', 'GET'])
@login_required
def pedidos_(id=None):
    if request.method == 'POST':
        name_client = request.form['name_client']
        payment = request.form['payment']
        address = request.form['address']
        delivery = request.form['delivery']
        tel = request.form['tel']
        note = request.form['note']
        pedidos.query.filter_by(id=id).update(
            {"name_client": name_client, "payment": payment, "address": address, "delivery": delivery, "tel": tel, "note": note})
        db.session.commit()
        return redirect('/painel/pedidos')

    menu_panel = load_menu()
    all_pedidos = pedidos.query.filter(
        pedidos.situation != 'FINALIZADO', pedidos.situation != 'CANCELADO').all()
    return render_template('panel/pedidos.html', menu_panel=menu_panel, all_pedidos=all_pedidos)


@bp.route('/cardapio/<case>/<int:id>', methods=['POST', 'GET'])
@bp.route('/cardapio', methods=['POST', 'GET'])
@login_required
def cardapio(id=None, case=None):

    if request.method == 'POST':

        if case != 'cancelar':
            title = request.form['title']
            amount = request.form['amount']
            situation = 'ATIVO'

        match case:

            case 'adicionais':
                adicional = adicionais(
                    title=title, amount=amount, situation=situation)
                db.session.add(adicional)
                flash(f'O adicional {title} foi adicionado com sucesso!')

            case 'produtos':
                description = request.form['description']
                file = request.files['file']

                if not file.filename == '':

                    if upload_image(file):
                        filename = file.filename.replace(' ', '_')

                    else:
                        flash(
                            'Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
                        return redirect('/painel/cardapio')

                else:
                    filename = 'product-default.webp'
                    flash('Imagem não encontrada, adicionamos uma padrão!')

                produto = produtos(
                    title=title, amount=amount, description=description, picture=filename, situation=situation)
                db.session.add(produto)
                flash(f'O produto {title} foi adicionado com sucesso!')

            case 'atualizar':
                produtos.query.filter_by(id=id).update(
                    {"title": title, "amount": amount, "description": description, "picture": filename, "situation": situation})
                flash(f'O produto {title} foi atualizado com sucesso!')

            case 'cancelar':
                situation = "CANCELADO"
                produtos.query.filter_by(id=id).update(
                    {"situation": situation})
                flash(f'O produto foi cancelado com sucesso!')

        db.session.commit()
        return redirect('/painel/cardapio')

    allProdutos = produtos.query.filter_by(situation='ATIVO').all()
    menu_panel = load_menu()
    return render_template('panel/cardapio.html', menu_panel=menu_panel, allProdutos=allProdutos)


@bp.route('/allOrders')
@login_required
def allOrders():
    menu_panel = load_menu()
    return render_template('panel/allOrders.html', menu_panel=menu_panel)


@bp.route('/<int:id>/<case>/change_order')
@login_required
def change_order(id, case):
    match case:
        case 'prepare':
            situation = "EM ANDAMENTO"
            order_start = datetime.now().strftime('%d-%m-%H %H:%M:%S')
            pedidos.query.filter_by(id=id).update(
                {"order_start": order_start, "situation": situation})
        case 'deliver':
            delivery = pedidos.query.filter_by(id=id).first()
            if delivery.delivery == 'ENTREGA':
                situation = "EM ENTREGA"
                pedidos.query.filter_by(id=id).update(
                    {"situation": situation})
            else:
                situation = "RETIRAR"
                pedidos.query.filter_by(id=id).update(
                    {"situation": situation})
        case 'finalize':
            situation = "FINALIZADO"
            pedidos.query.filter_by(id=id).update(
                {"situation": situation})
        case 'cancel':
            situation = "CANCELADO"
            pedidos.query.filter_by(id=id).update(
                {"situation": situation})

    db.session.commit()
    return redirect('/painel/pedidos')
