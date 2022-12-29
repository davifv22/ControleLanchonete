from app import *

bp = Blueprint('cad', __name__, url_prefix='/painel/cad')


@bp.route('/empresa', methods=['POST', 'GET'])
@login_required
def empresa():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/empresa.html', name_company=name_company, date=date, user=user)

@bp.route('/usuarios', methods=['POST', 'GET'])
@login_required
def usuarios():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/users.html', name_company=name_company, date=date, user=user)

@bp.route('/cardapio', methods=['POST', 'GET'])
@login_required
def cardapio():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/cardapio.html', name_company=name_company, date=date, user=user)

@bp.route('/fornecedores', methods=['POST', 'GET'])
@login_required
def fornecedores():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/fornecedores.html', name_company=name_company, date=date, user=user)

@bp.route('/config', methods=['POST', 'GET'])
@login_required
def config():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('Data: %d/%m/%Y')
    user = current_user.name
    return render_template('panel/config.html', name_company=name_company, date=date, user=user)