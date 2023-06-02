from app import *


def soma_itens_valor():
    itens_get = request.form.getlist('itens')
    itens = ''
    valor_custo = 0
    for item in itens_get:
        valor_item = produtosModel.produtos_itens.query.filter_by(titulo=item).first()
        valor_custo = valor_custo + float(valor_item.valor_venda)
        if itens == '':
            itens = item
            continue
        itens = f'{itens}, {item}'
    return itens, valor_custo


def add_produto():
    titulo = request.form.get('titulo')
    valor_venda = request.form.get('valor_venda')
    descricao = request.form.get('descricao')

    if not request.form.getlist('itens') == []:
        itens_valor = soma_itens_valor()
    else:
        return False

    situacao = 'ATIVO'
    file = request.files.get('file')
    if not file.filename == '':
        if uploads.upload_image(file):
            filename = file.filename.replace(' ', '_')
        else:
            flash(
                'Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
            return redirect('/painel/cardapio')
    else:
        filename = 'product-default.webp'
        flash('Imagem não encontrada, adicionamos uma padrão!')
    produto = produtosModel.produtos(titulo=titulo, valor_custo=itens_valor[1], valor_venda=valor_venda,
                       descricao=descricao, foto=filename, itens=itens_valor[0], situacao=situacao)
    db.session.add(produto)
    return True


def edit_produto(id):
    titulo = request.form['titulo']
    valor_venda = request.form['valor_venda']
    descricao = request.form['descricao']

    if not request.form.getlist('itens') == []:
        itens_valor = soma_itens_valor()
    else:
        return False

    file = request.files['file']
    if not file.filename == '':
        if uploads.upload_image(file):
            filename = file.filename.replace(' ', '_')
            produtosModel.produtos.query.filter_by(id=id).update(
                {"titulo": titulo, "valor_custo": itens_valor[1], "valor_venda": valor_venda, "descricao": descricao, "itens": itens_valor[0], "foto": filename})
        else:
            flash(
                'Extensão não suportada, a imagem deve ser .png, .jpg, .jpeg ou .webp')
            return redirect('/painel/cardapio')
    else:
        produtosModel.produtos.query.filter_by(id=id).update(
            {"titulo": titulo, "valor_custo": itens_valor[1], "valor_venda": valor_venda, "descricao": descricao, "itens": itens_valor[0]})
    return True


def delete_produto(id):
    situacao = "CANCELADO"
    produtosModel.produtos.query.filter_by(id=id).update(
        {"situacao": situacao})
    return True


def add_item():
    titulo = request.form['titulo']
    tipo_item = request.form['tipo_item']
    valor_custo = request.form['valor_custo']
    valor_venda = request.form['valor_venda']
    situacao = 'ATIVO'
    item = produtosModel.produtos_itens(titulo=titulo, tipo_item=tipo_item,
                          valor_custo=valor_custo, valor_venda=valor_venda, situacao=situacao)
    db.session.add(item)
    return True
