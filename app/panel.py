from app import *
from app.order import *
from app.product import *

bp = Blueprint('panel', __name__, url_prefix='/painel')


@bp.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass
    menu_panel = load_menu()
    values_panel = load_values_panel()
    return render_template('panel/home.html', menu_panel=menu_panel, values_panel=values_panel)


@bp.route('/pedido/<int:id>/<case>', methods=['POST', 'GET'])
@bp.route('/pedidos', methods=['POST', 'GET'])
@login_required
def pedidos_(id=None, case=None):
    if request.method == 'POST':
        match case:
            case 'prepare':
                prepare(id)
            case 'deliver':
                deliver(id)
            case 'finalize':
                finalize(id)
            case 'cancel':
                if cancel(id) is True:
                    flash(f'O pedido ID #{id} foi cancelado com sucesso!')
            case 'update':
                if update(id) is True:
                    flash(f'O pedido ID #{id} foi atualizado com sucesso!')
        db.session.commit()
        return redirect('/painel/pedidos')
    menu_panel = load_menu()
    all_pedidos = pedidos.query.filter(
        pedidos.situacao != 'FINALIZADO', pedidos.situacao != 'CANCELADO').all()
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
                if add_item() is True:
                    flash(f'O item {titulo} foi adicionado com sucesso!')
            case 'add':
                if add_produto() is True:
                    flash(f'O produto {titulo} foi adicionado com sucesso!')
                elif add_produto() is False:
                    flash('Selecione um item!')
            case 'edit':
                if edit_produto(id) is True:
                    flash(f'O produto {titulo} foi atualizado com sucesso!')
                elif edit_produto(id) is False:
                    flash('Selecione um item!')
            case 'cancel':
                if delete_produto(id) is True:
                    flash(f'O produto foi cancelado com sucesso!')
        db.session.commit()
        return redirect('/painel/cardapio')

    if request.method == 'GET':
        allProdutos = produtos.query.filter_by(situacao='ATIVO').all()
        item_Carnes = produtos_itens.query.filter_by(tipo_item='Carnes').all()
        item_Saladas = produtos_itens.query.filter_by(
            tipo_item='Saladas').all()
        item_Queijos = produtos_itens.query.filter_by(
            tipo_item='Queijos').all()
        item_Molhos = produtos_itens.query.filter_by(tipo_item='Molhos').all()
        menu_panel = load_menu()
    return render_template('panel/cardapio.html', menu_panel=menu_panel, allProdutos=allProdutos, item_Carnes=item_Carnes, item_Saladas=item_Saladas, item_Queijos=item_Queijos, item_Molhos=item_Molhos)
