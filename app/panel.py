from app import *

bp = Blueprint('panel', __name__, url_prefix='/painel')


@bp.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/home.html', name_company=name_company, date=date, user=user)


@bp.route('/pedidos', methods=['POST', 'GET'])
@login_required
def pedidos():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/pedidos.html', name_company=name_company, date=date, user=user)