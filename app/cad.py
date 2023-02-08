from app import *

bp = Blueprint('cad', __name__, url_prefix='/painel/cad')

@bp.route('/empresa', methods=['POST', 'GET'])
@login_required
def empresa():
    if request.method == 'POST':
        nome_empresa = request.form['nome_empresa']
        razao_social = request.form['razao_social']
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        cep = request.form['cep']
        email = request.form['email']
        tel = request.form['tel']
        cnpj = request.form['cnpj']
        if cadempresa.query.filter_by(id=1).first() is None:
            dt_criacao = datetime.now()
            add = cadempresa(nome_empresa=nome_empresa, razao_social=razao_social, endereco=endereco,
                             bairro=bairro, cidade=cidade, cep=cep, email=email, tel=tel, cnpj=cnpj, dt_criacao=dt_criacao)
            db.session.add(add)
        else:
            cadempresa.query.filter_by(id=1).update({"nome_empresa": nome_empresa, "razao_social": razao_social,
                                                     "endereco": endereco, "bairro": bairro, "cidade": cidade, "cep": cep, "email": email, "tel": tel, "cnpj": cnpj})
        db.session.commit()
        return redirect('/painel/cad/empresa')

    cad_empresa = cadempresa.query.filter_by(id=1).first()
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/empresa.html', menu_panel=menu_panel, cad_empresa=cad_empresa)


@bp.route('/usuarios', methods=['POST', 'GET'])
@login_required
def usuarios():
    if request.method == 'POST':
        pass
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/users.html', menu_panel=menu_panel)


@bp.route('/fornecedores', methods=['POST', 'GET'])
@login_required
def fornecedores():
    if request.method == 'POST':
        pass
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/fornecedores.html', menu_panel=menu_panel)


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
            controle.query.filter_by(id=1).update(
                {"debito": debito, "dt_ref": dt_ref})
        db.session.commit()
        return redirect('/painel/cad/config')

    config1 = controle.query.filter_by(id=1).first()
    menu_panel = panel.load_menu()
    return render_template('panel/config.html', config1=config1, menu_panel=menu_panel)


@bp.route('/addorder', methods=['POST', 'GET'])
@login_required
def addOrder():
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/addProduto.html', menu_panel=menu_panel)