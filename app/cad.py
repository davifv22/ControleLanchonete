from app import *

bp = Blueprint('cad', __name__, url_prefix='/painel/cad')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/empresa.html', menu_panel=menu_panel, cad_empresa=cad_empresa)


@bp.route('/usuarios', methods=['POST', 'GET'])
@login_required
def usuarios():
    if request.method == 'POST':
        pass
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/users.html', menu_panel=menu_panel)

@bp.route('/cardapio/<case>/<int:id>', methods=['POST', 'GET'])
@bp.route('/cardapio', methods=['POST', 'GET'])
@login_required
def cardapio(id=None, case=None):
    if request.method == 'POST':
        match case:
            case 'adicionais':
                title = request.form['title']
                amount = request.form['amount']
                situation = 'ATIVO'
                adicional = adicionais(title=title, amount=amount, situation=situation)
                db.session.add(adicional)
            case 'produtos':
                title = request.form['title']
                amount = request.form['amount']
                description = request.form['description']

                file = request.files['file']
                if not file.filename == '':
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    else:
                        flash('Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
                        return redirect('/painel/cad/cardapio')
                else:
                    filename = 'product-default.webp'
                    flash('Imagem não encontrada, adicionamos uma padrão!')
                
                situation = 'ATIVO'
                produto = produtos(title=title, amount=amount, description=description, picture=filename, situation=situation)
                db.session.add(produto)
        db.session.commit()
        return redirect('/painel/cad/cardapio')
    
    alladicionais = adicionais.query.filter_by(situation='ATIVO').all()
    menu_panel = panel.load_menu()
    return render_template('panel/cadastros/cardapio.html', menu_panel=menu_panel, alladicionais=alladicionais)

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