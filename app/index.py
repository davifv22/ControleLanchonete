from app import *

bp = Blueprint('index', __name__)


def load_menu_index():
    empresa = cadempresa.query.filter_by(id=1).first()
    if empresa is None:
        company_name = 'NOME EMPRESA'
    else:
        company_name = empresa.company_name
    return company_name


@bp.route('/', methods=['POST', 'GET'])
def index_():
    if request.method == 'POST':
        name_client = request.form['name_client']
        delivery = request.form['delivery']
        amount = request.form['amount']
        payment = request.form['payment']
        note = request.form['note']
        address = request.form['address']
        tel = request.form['tel']
        order_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        situation = 'PENDENTE'
        add = pedidos(name_client=name_client, delivery=delivery, amount=amount, payment=payment, note=note,
                      address=address, tel=tel, order_time=order_time, order_start='', situation=situation)
        db.session.add(add)
        db.session.commit()
        return redirect('/')

    menu_panel = load_menu_index()
    return render_template('index/index.html', menu_panel=menu_panel)
