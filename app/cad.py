from app import *

bp = Blueprint('cad', __name__, url_prefix='/painel/cad')


@bp.route('/empresa', methods=['POST', 'GET'])
@login_required
def empresa():
    if request.method == 'POST':
        company_name = request.form['company_name']
        corporate_name = request.form['corporate_name']
        address = request.form['address']
        district = request.form['district']
        city = request.form['city']
        cep = request.form['cep']
        email = request.form['email']
        tel = request.form['tel']
        cnpj = request.form['cnpj']
        if cadempresa.query.filter_by(id=1).first() is None:
            dt_create = datetime.now()
            add = cadempresa(company_name=company_name, corporate_name=corporate_name, address=address,
                             district=district, city=city, cep=cep, email=email, tel=tel, cnpj=cnpj, dt_create=dt_create)
            db.session.add(add)
        else:
            cadempresa.query.filter_by(id=1).update({"company_name": company_name, "corporate_name": corporate_name,
                                                     "address": address, "district": district, "city": city, "cep": cep, "email": email, "tel": tel, "cnpj": cnpj})
        db.session.commit()
        return redirect('/painel/cad/empresa')

    cad_empresa = cadempresa.query.filter_by(id=1).first()

    name_company = "Nome empresa"
    date = datetime.now().strftime('%d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/empresa.html', name_company=name_company, date=date, user=user, cad_empresa=cad_empresa)


@bp.route('/usuarios', methods=['POST', 'GET'])
@login_required
def usuarios():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('%d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/users.html', name_company=name_company, date=date, user=user)


@bp.route('/cardapio', methods=['POST', 'GET'])
@login_required
def cardapio():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('%d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/cardapio.html', name_company=name_company, date=date, user=user)


@bp.route('/fornecedores', methods=['POST', 'GET'])
@login_required
def fornecedores():
    if request.method == 'POST':
        pass
    name_company = "Nome empresa"
    date = datetime.now().strftime('%d/%m/%Y')
    user = current_user.name
    return render_template('panel/cadastros/fornecedores.html', name_company=name_company, date=date, user=user)


@bp.route('/config', methods=['POST', 'GET'])
@login_required
def config():
    if request.method == 'POST':
        debito = request.form['debito']
        dt_ref = request.form['dt_ref']
        if controle.query.filter_by(id=1).first() is None:
            add = controle(debito=debito, dt_ref=dt_ref)
            db.session.add(add)
        else:
            controle.query.filter_by(id=1).update({"debito": debito, "dt_ref": dt_ref})
        db.session.commit()
        return redirect('/painel/cad/empresa')
            
        
        
    name_company = "Nome empresa"
    date = datetime.now().strftime('%d/%m/%Y')
    user = current_user.name
    return render_template('panel/config.html', name_company=name_company, date=date, user=user)
