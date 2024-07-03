from flask import Flask, jsonify, request, make_response
from databse import db_session, init_db
from models import Pedido

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/livros', methods=['GET'])
def obter_livros():
    livros = []
    for livro in Pedido.query.all():
        livros.append({"livro": livro.as_dict(), "link: ": "http://localhost:5000/livro/{}".format(livro.id)})
    return make_response(jsonify(livros), 200)

@app.route('/livro/<int:id>', methods=['GET'])
def obter_livros_por(id):
    try:
        livro = Pedido.query.get(id)
        if livro != "" and livro != None:
            livro = livro.as_dict()
            return make_response(jsonify({"Status code": 200, "data": livro, "link: ": "http://localhost:5000/livros"}), 200)
        else:
            return make_response(jsonify({"Status code": 400, "data": "Livro não encontrado!"}), 400)
    except:
        return make_response(jsonify({"Status code": 400, "data": "Livro não encontrado!"}), 400)
    
@app.route('/livro/add', methods=['POST'])
def adicionar_livro():
    input_livro = request.get_json()
    try:
        if input_livro['titulo'] != "" and input_livro['autor'] != "":
            livro_novo = Pedido(input_livro['titulo'], input_livro['autor'])
            db_session.add(livro_novo)
            db_session.commit()
            return make_response(jsonify({"Status code: ": 200, "Messenger": "Livro adicionado com sucesso!","data": livro_novo.as_dict()}), 200)
        else:
            return make_response(jsonify({"Status code": 400, "Messenger": "Erro ao inserir Livro!", "data": input_livro}), 400)
    except:
        return make_response(jsonify({"Status code": 400, "Messenger": "Erro ao inserir Livro!", "data": input_livro}), 400)

@app.route('/livro/delete/<int:id>', methods=['DELETE'])
def delet_livro(id):
    livro = Pedido.query.get(id)
    if livro != "" and livro != None:
        db_session.delete(livro)
        db_session.commit()
        return make_response(jsonify({"Status code": 200, "Messenger": "Deletado com sucesso!", "data": livro.as_dict()}), 200)
    else:
        return make_response(jsonify({"Status code": 400, "Messenger": "Error ao deletar!", "data": livro}), 400)

@app.route('/livro/edit/<int:id>', methods=['PUT'])
def edit_livro(id):
    livro = Pedido.query.get(id)
    try:
        if livro != "" and livro != None:
            livro_update = request.get_json()
            livro.titulo = livro_update['titulo']
            livro.autor = livro_update['autor']
            db_session.commit()
            return make_response(jsonify({"Status code: ":200, "Messenger":"Livro alterado com sucesso!", "data": livro_update}), 200)
        else:
            return make_response(jsonify({"Status code: ":400, "Messenger":"Falha ao alterar o livro!", "data": livro}), 400)
    except:
        return make_response(jsonify({"Status code: ":400, "Messenger":"Falha ao alterar o livro!", "data": livro}), 400)

if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)