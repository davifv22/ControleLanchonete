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
        pedidos.situation != 'FINALIZADO', pedidos.situation != 'CANCELADO').all()
    return render_template('panel/pedidos.html', menu_panel=menu_panel, all_pedidos=all_pedidos)


@bp.route('/cardapio/<case>/<int:id>', methods=['POST', 'GET'])
@bp.route('/cardapio', methods=['POST', 'GET'])
@login_required
def cardapio(id=None, case=None):
    if request.method == 'POST':
        if not case == 'cancel':
            title = request.form['title']
        match case:
            case 'adicionais':
                if addtional() is True:
                    flash(f'O adicional {title} foi adicionado com sucesso!')
            case 'add':
                if add_produto() is True:
                    flash(f'O produto {title} foi adicionado com sucesso!')
            case 'edit':
                if edit_produto(id) is True:
                    flash(f'O produto {title} foi atualizado com sucesso!')
            case 'cancel':
                if delete_produto(id) is True:
                    flash(f'O produto foi cancelado com sucesso!')
        db.session.commit()
        return redirect('/painel/cardapio')

    allProdutos = produtos.query.filter_by(situation='ATIVO').all()
    menu_panel = load_menu()
    return render_template('panel/cardapio.html', menu_panel=menu_panel, allProdutos=allProdutos)
