from app import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        senha = request.form['senha']
        user_query = users.query.filter_by(user=user).first()

        if user_query is None:
            #criar mensagem que usur nao existe
            return redirect('/auth/login')

        if senha == user_query.senha:
            login_user(user_query)
            return redirect('/painel/home')
        else:
            # criar mensagem de senha ou usuario incorreto
            return redirect('/auth/login')

    logout_user()
    return render_template('auth/login.html')

@bp.route('/register',methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        situacao = 'ATIVO'
        administrador = 'SIM'
        dt_criacao = datetime.now()
        add = users(user=user,nome=nome,email=email,senha=senha,administrador=administrador,situacao=situacao, dt_criacao=dt_criacao)
        db.session.add(add)
        db.session.commit()
        user = users.query.filter_by(user=user).first()
        login_user(user)
        return redirect('/painel/home')
    return render_template('auth/register.html')


@bp.route('/logout',methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/auth/login')