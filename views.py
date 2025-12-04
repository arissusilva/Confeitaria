from flask import render_template, request

def init_app(app):

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/pedido')
    def pedido():
        pizzas = [
            {"nome": "Pepperoni", "descricao": "Molho, mussarela e pepperoni.", "img_file": "pepperoni.jpg"},
            {"nome": "4 Queijos", "descricao": "Molho, mussarela, gorgonzola, parmesão e cheddar.", "img_file": "4queijos.jpg"},
            {"nome": "Marguerita", "descricao": "Molho, mussarela, tomate e manjericão.", "img_file": "marguerita.jpg"},
            {"nome": "Carne", "descricao": "Molho, mussarela e carne desfiado.", "img_file": "carne.jpg"},
            {"nome": "Champignon", "descricao": "Molho, mussarela, champignon e azeitona.", "img_file": "champignon.jpg"},
            {"nome": "Atum", "descricao": "Molho, mussarela, atum, cebola e azeitona.", "img_file": "atum.jpg"},
            {"nome": "Shitake", "descricao": "Molho, mussarela, shitake e azeitona.", "img_file": "shitake.jpg"},
            {"nome": "Chocolate", "descricao": "Mussarela, chocolate.", "img_file": "chocolate.jpeg"},
        ]
        return render_template("pedido.html", pizzas=pizzas)

    @app.route('/finalizar_pedido', methods=["POST"])
    def finalizar_pedido():

        sabores = request.form.getlist("sabores")
        tamanho = request.form.get("tamanho")

        return render_template(
            "finalizar.html",
            sabores=sabores,
            tamanho=tamanho
        )
