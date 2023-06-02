from app import *

bp = Blueprint('panel', __name__, url_prefix='/painel')


@bp.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass
    menu_panel = load.menu.get()
    values_panel = load.values_panel.get()
    return render_template('panel/home.html', menu_panel=menu_panel, values_panel=values_panel)


@bp.route('/pedido/<int:id>/<case>', methods=['POST', 'GET'])
@bp.route('/pedidos', methods=['POST', 'GET'])
@login_required
def pedidos_(id=None, case=None):
    if request.method == 'POST':
        match case:
            case 'prepare':
                order.prepare(id)
            case 'deliver':
                order.deliver(id)
            case 'finalize':
                order.finalize(id)
            case 'cancel':
                if order.cancel(id) is True:
                    flash(f'O pedido ID #{id} foi cancelado com sucesso!')
            case 'update':
                if order.update(id) is True:
                    flash(f'O pedido ID #{id} foi atualizado com sucesso!')
        db.session.commit()
        return redirect('/painel/pedidos')
    menu_panel = load.menu.get()
    all_pedidos = pedidosModel.pedidos.query.filter(pedidosModel.pedidos.situacao != 'FINALIZADO', pedidosModel.pedidos.situacao != 'CANCELADO').all()
    return render_template('panel/pedidos.html', menu_panel=menu_panel, all_pedidos=all_pedidos)


@bp.route('/cardapio/<case>/<int:id>', methods=['POST'])
@bp.route('/cardapio', methods=['GET'])
@login_required
def cardapio(id=None, case=None):
    if request.method == 'POST':
        if not case == 'cancel':
            titulo = request.form['titulo']
        match case:
            case 'add_item':
                if product.add_item() is True:
                    flash(f'O item {titulo} foi adicionado com sucesso!')
            case 'add':
                if product.add_produto() is True:
                    flash(f'O produto {titulo} foi adicionado com sucesso!')
                elif product.add_produto() is False:
                    flash('Selecione um item!')
            case 'edit':
                if product.edit_produto(id) is True:
                    flash(f'O produto {titulo} foi atualizado com sucesso!')
                elif product.edit_produto(id) is False:
                    flash('Selecione um item!')
            case 'cancel':
                if product.delete_produto(id) is True:
                    flash(f'O produto foi cancelado com sucesso!')
        db.session.commit()
        return redirect('/painel/cardapio')

    if request.method == 'GET':
        allProdutos = produtosModel.produtos.query.filter_by(situacao='ATIVO').all()
        item_Carnes = produtosModel.produtos_itens.query.filter_by(tipo_item='Carnes').all()
        item_Saladas = produtosModel.produtos_itens.query.filter_by(
            tipo_item='Saladas').all()
        item_Queijos = produtosModel.produtos_itens.query.filter_by(
            tipo_item='Queijos').all()
        item_Molhos = produtosModel.produtos_itens.query.filter_by(tipo_item='Molhos').all()
        menu_panel = load.menu.get()
    return render_template('panel/cardapio.html', menu_panel=menu_panel, allProdutos=allProdutos, item_Carnes=item_Carnes, item_Saladas=item_Saladas, item_Queijos=item_Queijos, item_Molhos=item_Molhos)
