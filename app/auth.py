from app import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        user_ = users.query.filter_by(user=user).first()

        if user_ is None:
            #criar mensagem que usur nao existe
            return redirect('/auth/login')

        if password == user_.password:
            login_user(user_)
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
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dt_create = datetime.now()
        situacao = 'A'
        add = users(user=user,name=name,email=email,password=password,dt_create=dt_create,situacao=situacao)
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