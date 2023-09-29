from app import *

bp = Blueprint('index', __name__)


@bp.route('/', methods=['POST', 'GET'])
def index_():
    if request.method == 'POST':
        nome_cliente = request.form['nome_cliente']
        sub_total = ''
        tipo_entrega = request.form['tipo_entrega']
        total = request.form['sub_total']
        total_itens = ''
        pagamento = request.form['pagamento']
        endereco = request.form['endereco']
        tel = request.form['tel']
        dt_pedido = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        add = pedidosModel.pedidos(nome_cliente=nome_cliente, sub_total=sub_total, tipo_entrega=tipo_entrega, total=total, total_itens=total_itens,
                      pagamento=pagamento, endereco=endereco, tel=tel, dt_pedido=dt_pedido, dt_inicio='', dt_concluido='', situacao='PENDENTE')
        db.session.add(add)
        db.session.commit()
        return redirect('/')

    itens_disponiveis = ('1','2','3','4','5') #todos produtos disponiveis
    menu_panel = load.menu_index.get()
    return render_template('index/index.html', menu_panel=menu_panel, itens_disponiveis=itens_disponiveis)
