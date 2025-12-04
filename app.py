# Importamos as ferramentas do Flask
# jsonify: essencial para enviar a resposta em formato JSON para o JavaScript do carrinho
from flask import Flask, render_template, request, jsonify

# Inicializamos o aplicativo
app = Flask(__name__)

# --- BANCO DE DADOS DO RABUDINHO (Com Preços Individuais) ---
# Adicionei o campo "preco" em cada item para permitir valores variados.

cardapio_bolo = [
    {
        "nome": "Chocolatudo",
        "categoria": "Bolo de Pote",
        "descricao": "Massa molhadinha com recheio de chocolate 50% Cacau.",
        "preco": 15.00, # Preço padrão
        "img_file": "bolo_chocolate.png" 
    },
    {
        "nome": "Choconinho",
        "categoria": "Bolo de Pote",
        "descricao": "Massa de chocolate com creme de ninho. O queridinho!",
        "preco": 16.50, # Um pouco mais caro
        "img_file": "bolo_ninho.jpg"
    },
    {
        "nome": "Beijinho de Coco",
        "categoria": "Bolo de Pote",
        "descricao": "Massa branca com recheio de beijinho e coco ralado.",
        "preco": 15.00,
        "img_file": "bolo_beijinho.jpg"
    }
]

cardapio_empada = [
    {
        "nome": "Empada de Frango",
        "categoria": "Empada",
        "descricao": "Recheio cremoso de frango com catupiry.",
        "preco": 8.00, # Preço padrão
        "img_file": "empadafrango.png"
    },
    {
        "nome": "Empada de Camarão",
        "categoria": "Empada",
        "descricao": "Camarão fresco com tempero especial.",
        "preco": 10.00, # Mais caro por ser fruto do mar
        "img_file": "empadacamarão.png"
    },
    {
        "nome": "Empada Doce",
        "categoria": "Empada",
        "descricao": "Opção vegetariana deliciosa.",
        "preco": 8.50,
        "img_file": "empadadoce.png"
    },
]

cardapio_trufa = [
    {
        "nome": "Trufa de Maracujá",
        "categoria": "Trufa",
        "descricao": "Chocolate meio amargo com recheio azedinho.",
        "preco": 5.00,
        "img_file": "maracuja.png"
    },
    {
        "nome": "Trufa de Morango",
        "categoria": "Trufa",
        "descricao": "Clássica trufa com pedaços de fruta.",
        "preco": 5.00,
        "img_file": "morango.png"
    },
    {
        "nome": "Trufa de Chocolate",
        "categoria": "Trufa",
        "descricao": "Intensa e cremosa.",
        "preco": 5.00,
        "img_file": "chocolatetrufa.png"
    },
    {
        "nome": "Trufa de Paçoca",
        "categoria": "Trufa",
        "descricao": "Recheio de amendoim cremoso.",
        "preco": 5.50,
        "img_file": "pacoca.png"
    },
    {
        "nome": "Trufa de Limão",
        "categoria": "Trufa",
        "descricao": "Chocolate branco com raspas de limão.",
        "preco": 5.00,
        "img_file": "trufalimao.png"
    },
]

# --- ROTAS DO SITE ---

# Rota Principal (Home)
@app.route('/')
def index():
    return render_template('home.html')

# Rota de Pedidos
@app.route('/pedido')
def fazer_pedido():
    # Juntamos todas as listas em uma só para enviar ao HTML
    todos_produtos = cardapio_bolo + cardapio_empada + cardapio_trufa
    return render_template('pedido.html', produtos=todos_produtos)

# Rota de Finalização (Processamento do Carrinho)
@app.route('/finalizar_pedido', methods=['POST'])
def finalizar():
    # Recebe os dados JSON do Javascript
    dados = request.get_json()
    carrinho = dados.get('carrinho')
    
    total_pedido = 0
    resumo_html = ""

    print("--- NOVO PEDIDO ---")
    
    for lote in carrinho:
        categoria = lote['categoria']
        itens_do_lote = lote['itens'] 
        
        subtotal_lote = 0
        detalhes_sabores = []

        for item in itens_do_lote:
            nome_sabor = item['nome']
            quantidade = item['qtd']
            preco_unitario = item['preco']
            
            valor_item = quantidade * preco_unitario
            subtotal_lote += valor_item
            
            detalhes_sabores.append(f"{quantidade}x {nome_sabor} (R$ {preco_unitario:.2f})")

        total_pedido += subtotal_lote
        sabores_str = "<br>".join(detalhes_sabores)
        
        resumo_html += f"""
        <li style="margin-bottom: 10px;">
            <strong>{categoria}</strong><br>
            {sabores_str}<br>
            <small style="color: #666;">Subtotal: R$ {subtotal_lote:.2f}</small>
        </li>
        """

    # 2. AQUI ESTÁ O USO DO JSONIFY
    # Retorna um objeto JSON contendo o HTML que será injetado na página
    return jsonify({
        "mensagem": "Sucesso",
        "html": f"""
        <div style="font-family: sans-serif; text-align: center; padding: 50px; color: #FFFDF0;">
            <h1 style="font-family: 'Pacifico', cursive; color: #FFFDF0; margin-bottom: 20px;">Pedido Recebido! 🍬</h1>
            <p style="font-size: 1.2em;">A equipe <strong>Doces do Rabudinho</strong> agradece a preferência.</p>
            
            <div class="caixa-resumo">
                <ul style="text-align: left; display: inline-block; line-height: 1.6; width: 100%;">
                    {resumo_html}
                </ul>
                <hr style="border-color: #eee; margin: 20px 0;">
                <h2 style="color: #2e7d32; font-size: 1.8em;">Total a Pagar: R$ {total_pedido:.2f}</h2>
            </div>

            <br>
            <p style="font-size: 1.1em;">Seu pedido está sendo preparado com muito carinho!</p>
            <br>
            <a href="/" class="botao-voltar">Voltar ao Início</a>
        </div>
        """
    })

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)