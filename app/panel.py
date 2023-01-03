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


@bp.route('/pedidos', methods=['POST', 'GET'])
@login_required
def pedidos_():
    if request.method == 'POST':
        pass

    menu_panel = load_menu()
    all_pedidos = pedidos.query.filter(pedidos.situation != 'FINALIZADO').all()
    return render_template('panel/pedidos.html', menu_panel=menu_panel, all_pedidos=all_pedidos)


@bp.route('/cardapio', methods=['POST', 'GET'])
@login_required
def cardapio():
    if request.method == 'POST':
        pass
    menu_panel = load_menu()
    return render_template('panel/cardapio.html', menu_panel=menu_panel)


# FUNÇÕES COM VARIAVEIS GLOBAIS
def load_menu():
    empresa = cadempresa.query.filter_by(id=1).first()
    if empresa is None:
        company_name = 'NOME EMPRESA'
    else:
        company_name = empresa.company_name
    username = current_user.name
    return username, company_name


def load_values_panel():
    # debito
    debito = db.session.query(db.func.sum(controle.debito)).scalar()
    if db.session.query(db.func.sum(pedidos.amount)).scalar() is None:
        faturamento = 0
    else:
        faturamento = db.session.query(
            db.func.sum(pedidos.amount)).scalar()
    # if db.session.query(db.func.sum(compras.valor_total)).scalar() is None:
    despesas = -10.00
    # else:
    #     despesas = db.session.query(db.func.sum(compras.valor_total)).scalar()
    total = float(debito) + float(faturamento) - float(despesas)
    return locale.currency(debito, grouping=True), locale.currency(faturamento, grouping=True), locale.currency(despesas, grouping=True), locale.currency(total, grouping=True)
