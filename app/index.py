from app import *

bp = Blueprint('index', __name__)


def load_menu_index():
    empresa = cadempresa.query.filter_by(id=1).first()
    if empresa is None:
        nome_empresa = 'NOME EMPRESA'
    else:
        nome_empresa = empresa.nome_empresa
    return nome_empresa


@bp.route('/', methods=['POST', 'GET'])
def index_():
    if request.method == 'POST':
        nome_cliente = request.form['nome_cliente']
        sub_total = ''
        tipo_entrega = request.form['tipo_entrega']
        total = request.form['total']
        total_itens = ''
        pagamento = request.form['pagamento']
        endereco = request.form['endereco']
        tel = request.form['tel']
        dt_pedido = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        add = pedidos(nome_cliente=nome_cliente, sub_total=sub_total, tipo_entrega=tipo_entrega, total=total, total_itens=total_itens,
                      pagamento=pagamento, endereco=endereco, tel=tel, dt_pedido=dt_pedido, dt_inicio='', dt_concluido='', situacao='PENDENTE')
        db.session.add(add)
        db.session.commit()
        return redirect('/')

    itens_disponiveis = ('1','2','3','4','5') #todos produtos disponiveis
    menu_panel = load_menu_index()
    return render_template('index/index.html', menu_panel=menu_panel, itens_disponiveis=itens_disponiveis)
