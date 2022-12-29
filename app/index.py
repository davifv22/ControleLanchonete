from app import *

bp = Blueprint('index', __name__)


@bp.route('/',methods=['POST', 'GET'])
def index_():
    if request.method == 'POST':
        name_client = request.form['name_client']
        items = request.form['items']
        address = request.form['address']
        tel = request.form['tel']
        order_time = datetime.now()
        situation = 'PENDENTE'
        add = pedidos(name_client=name_client, items=items, address=address, tel=tel, order_time=order_time, situation=situation)
        db.session.add(add)
        db.session.commit()
        return redirect('/')
        
    name_company = "Nome empresa"
    return render_template('index/index.html', name_company=name_company)