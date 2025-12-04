# Importamos o Flask e suas ferramentas
# render_template: para mostrar o HTML
# request: para receber os dados do formulário de pedido
from flask import Flask, render_template, request

# Inicializamos o aplicativo Flask
app = Flask(__name__)

# --- BANCO DE DADOS DO RABUDINHO (Simulado) ---
# Lista de dicionários contendo os nossos doces maravilhosos.
# Importante: As imagens (img_file) devem existir na pasta static/img
# --- BANCO DE DADOS DO RABUDINHO ---
cardapio_bolo = [
    # --- BOLOS DE POTE ---
    {
        "nome": "Chocolatudo",
        "categoria": "Bolo de Pote",
        "descricao": "Massa molhadinha com recheio de chocolate 50% Cacau.",
        "img_file": "bolo_chocolate.png" 
    },
    {
        "nome": "Choconinho",
        "categoria": "Bolo de Pote",
        "descricao": "O queridinho da galera. Muito recheio! Massa de chocolate com creme de ninho.",
        "img_file": "bolo_ninho.jpg"
    },
    {
        "nome": "Beijinho de Coco",
        "categoria": "Bolo de Pote",
        "descricao": "Massa branca com recheio de beijinho e coco ralado.",
        "img_file": "bolo_beijinho.jpg"
    },
    {
        "nome": "Choconinho",
        "categoria": "Bolo de Pote",
        "descricao": "O queridinho da galera. Muito recheio! Massa de chocolate com creme de ninho.",
        "img_file": "bolo_ninho.jpg"
    },
]
cardapio_empada = [
    # --- EMPADAS ---
    {
        "nome": "Empada de Frango",
        "categoria": "Empada",
        "descricao": "Recheio cremoso de frango com catupiry.",
        "img_file": "empadafrango.png"
    },
    {
        "nome": "Empada de Camarão",
        "categoria": "Empada",
        "descricao": "Camarão fresco com tempero especial.",
        "img_file": "empadacamarão.png"
    },
    {
        "nome": "Empada Doce",
        "categoria": "Empada",
        "descricao": "Opção vegetariana deliciosa.",
        "img_file": "empadadoce.png"
    },
]
cardapio_trufa = [
    # --- TRUFAS ---
    {
        "nome": "Trufa de Maracujá",
        "categoria": "Trufa",
        "descricao": "Chocolate meio amargo com recheio azedinho.",
        "img_file": "maracuja.png"
    },
    {
        "nome": "Trufa de Morango",
        "categoria": "Trufa",
        "descricao": "Clássica trufa com pedaços de fruta.",
        "img_file": "morango.png"
    },
    {
        "nome": "Trufa de Chocolate",
        "categoria": "Trufa",
        "descricao": "Clássica trufa com pedaços de fruta.",
        "img_file": "chocolatetrufa.png"
    },
    {
        "nome": "Trufa de Paçoca",
        "categoria": "Trufa",
        "descricao": "Clássica trufa com pedaços de fruta.",
        "img_file": "pacoca.png"
    },
    {
        "nome": "Trufa de Limão",
        "categoria": "Trufa",
        "descricao": "Clássica trufa com pedaços de fruta.",
        "img_file": "trufalimao.png"
    },
]

# --- ROTAS DO SITE ---

# Rota da Página Inicial (Home)
@app.route('/')
def index():
    # Renderiza o arquivo home.html (a fachada da loja)
    return render_template('home.html')

# Rota da Página de Pedidos (Onde o cliente escolhe os doces)
@app.route('/pedido')
def fazer_pedido():
    # Renderiza o pedido.html
    # Enviamos a lista 'cardapio_doces' para o HTML usar no loop {% for %}
    # Note que no HTML você vai chamar de 'pizzas' ou mudar lá para 'doces'
    # Para facilitar, vou enviar com o nome genérico 'produtos'
    return render_template('pedido.html', produtos=cardapio_bolo + cardapio_empada + cardapio_trufa)

# Rota que processa o pedido (Botão Finalizar)
@app.route('/finalizar_pedido', methods=['POST'])
def finalizar():
    # Agora recebemos um JSON (um pacote de dados do Javascript)
    dados = request.get_json()
    carrinho = dados.get('carrinho')
    
    total_pedido = 0
    resumo_html = ""

    # Dicionário de preços para conferência no servidor
    tabela_precos = {
        "Bolo de Pote": 15.00,
        "Empada": 8.00,
        "Trufa": 5.00
    }

    print("--- NOVO PEDIDO CARRINHO ---")
    
    # Processa item por item do carrinho
    for item in carrinho:
        categoria = item['categoria']
        sabores = item['sabores']
        
        preco_unitario = tabela_precos.get(categoria, 0)
        total_pedido += preco_unitario
        
        # Monta o visual para o terminal e para a resposta
        sabores_str = ", ".join(sabores)
        print(f"Item: {categoria} | Sabores: {sabores_str} | R$ {preco_unitario}")
        
        resumo_html += f"<li><strong>{categoria}</strong> ({sabores_str}) - R$ {preco_unitario:.2f}</li>"

    print(f"TOTAL: R$ {total_pedido:.2f}")

    # Resposta que vai aparecer na tela do cliente
    return jsonify({
        "mensagem": "Sucesso",
        "html": f"""
        <div style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #8a3106;">Pedido Recebido! 🍬</h1>
            <p>A equipe <strong>Doces do Rabudinho</strong> agradece.</p>
            <hr>
            <ul style="text-align: left; display: inline-block;">
                {resumo_html}
            </ul>
            <h2 style="color: #2e7d32;">Total a Pagar: R$ {total_pedido:.2f}</h2>
            <br>
            <a href="/" style="background: #8a3106; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Voltar ao Início</a>
        </div>
        """
    })

# Inicia o servidor se o arquivo for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)