from app import *


def add_produto():
    title = request.form['title']
    amount = request.form['amount']
    situation = 'ATIVO'
    description = request.form['description']
    file = request.files['file']
    if not file.filename == '':
        if upload_image(file):
            filename = file.filename.replace(' ', '_')
        else:
            flash(
                'Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
            return redirect('/painel/cardapio')
    else:
        filename = 'product-default.webp'
        flash('Imagem não encontrada, adicionamos uma padrão!')
    produto = produtos(
        title=title, amount=amount, description=description, picture=filename, situation=situation)
    db.session.add(produto)
    return True


def edit_produto(id):
    title = request.form['title']
    amount = request.form['amount']
    description = request.form['description']
    file = request.files['file']
    if not file.filename == '':
        if upload_image(file):
            filename = file.filename.replace(' ', '_')
            produtos.query.filter_by(id=id).update(
                {"title": title, "amount": amount, "description": description, "picture": filename})
        else:
            flash(
                'Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
            return redirect('/painel/cardapio')
    else:
        produtos.query.filter_by(id=id).update(
            {"title": title, "amount": amount, "description": description})
    return True


def delete_produto(id):
    situation = "CANCELADO"
    produtos.query.filter_by(id=id).update(
        {"situation": situation})
    return True


def addtional(id, case):
    pass
