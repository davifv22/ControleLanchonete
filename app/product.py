from app import *


def add_produto():
    titulo = request.form['titulo']
    valor_custo = '' # soma dos itens add
    valor_venda = request.form['valor_venda']
    descricao = request.form['descricao']
    itens = []
    situacao = 'ATIVO'
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
    produto = produtos(titulo=titulo, valor_custo=valor_custo, valor_venda=valor_venda, descricao=descricao, foto=filename, itens=itens, situacao=situacao)
    db.session.add(produto)
    return True


def edit_produto(id):
    titulo = request.form['titulo']
    valor_venda = request.form['valor_venda']
    descricao = request.form['descricao']
    itens = ''
    
    file = request.files['file']
    if not file.filename == '':
        if upload_image(file):
            filename = file.filename.replace(' ', '_')
            produtos.query.filter_by(id=id).update(
                {"titulo": titulo, "valor_venda": valor_venda, "descricao": descricao, "itens": itens, "foto": filename})
        else:
            flash(
                'Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
            return redirect('/painel/cardapio')
    else:
        produtos.query.filter_by(id=id).update(
            {"titulo": titulo, "valor_venda": valor_venda, "descricao": descricao, "itens": itens})
    return True


def delete_produto(id):
    situacao = "CANCELADO"
    produtos.query.filter_by(id=id).update(
        {"situacao": situacao})
    return True


def add_item(id, case):
    pass
