from app import *


@app.route('/create_db', methods=['POST', 'GET'])
def create():
    # Criar pagina para montar tabela controle (versões, nome loja, contato e etc...)
    db.create_all()
    return redirect('/auth/login')
