# Importa os recursos do Flask usados pela aplicação.
from flask import Flask, render_template, request, redirect, url_for, flash
# Importa o módulo os para ler variáveis de ambiente.
import os
import time
# Importa o conector oficial usado para acessar o MySQL a partir do Python.
import mysql.connector
# Importa o tipo de erro do conector para tratar falhas de banco de dados.
from mysql.connector import Error

# Cria a aplicação Flask.
app = Flask(__name__)
# Define uma chave simples para permitir o uso de mensagens flash nesta aula.
app.secret_key = "aula-compose-flask-mysql"

# Cria uma função que abre uma nova conexão com o banco de dados.
def conectar_banco():
    # Retorna uma conexão usando as variáveis recebidas pelo Docker Compose.
    return mysql.connector.connect(
        # Usa o nome do serviço db como hostname dentro da rede do Compose.
        host=os.getenv("DB_HOST", "db"),
        # Converte a porta recebida como texto para número inteiro.
        port=int(os.getenv("DB_PORT", "3306")),
        # Define o nome do banco que será utilizado.
        database=os.getenv("DB_NAME", "cadastro_db"),
        # Define o usuário da aplicação.
        user=os.getenv("DB_USER", "cadastro_user"),
        # Define a senha do usuário da aplicação.
        password=os.getenv("DB_PASSWORD", "cadastro123")
    )


def criar_tabela_cadastros(retries: int = 10, delay: int = 3):
    """Tenta criar a tabela `cadastros` no banco. Faz várias tentativas caso o MySQL ainda não esteja disponível."""
    sql = """
    CREATE TABLE IF NOT EXISTS cadastros (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome_responsavel VARCHAR(100) NOT NULL,
        telefone VARCHAR(20),
        email VARCHAR(150) NOT NULL,
        sneaker_nome VARCHAR(100) NOT NULL,
        marca VARCHAR(50),
        modelo VARCHAR(50),
        tipo VARCHAR(50),
        tamanho VARCHAR(10),
        cor VARCHAR(50),
        observacoes TEXT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    attempt = 0
    while attempt < retries:
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute(sql)
            conexao.commit()
            cursor.close()
            conexao.close()
            print("Tabela 'cadastros' verificada/criada com sucesso.")
            return
        except Error as erro:
            attempt += 1
            print(f"Tentativa {attempt}/{retries} - erro ao criar tabela: {erro}")
            time.sleep(delay)
    print("Falha ao criar a tabela 'cadastros' após múltiplas tentativas.")

# Define a rota principal da aplicação.
@app.route("/")
def index():
    # Cria uma lista vazia caso a consulta não possa ser realizada.
    usuarios = []
    # Inicia um bloco protegido para tratar possíveis erros do MySQL.
    try:
        # Abre a conexão com o banco.
        conexao = conectar_banco()
        # Cria um cursor que devolve cada linha como dicionário.
        cursor = conexao.cursor(dictionary=True)
        # Consulta os usuários cadastrados, do mais recente para o mais antigo.
        cursor.execute("SELECT id, nome, email, criado_em FROM usuarios ORDER BY id DESC")
        # Armazena todas as linhas retornadas pela consulta.
        usuarios = cursor.fetchall()
        # Fecha o cursor após a consulta.
        cursor.close()
        # Fecha a conexão após a consulta.
        conexao.close()
    # Captura erros gerados pelo conector MySQL.
    except Error as erro:
        # Mostra uma mensagem amigável na página.
        flash(f"Erro ao consultar o banco: {erro}", "erro")
    # Renderiza a página e envia a lista de usuários para o HTML.
    return render_template("index.html", usuarios=usuarios)


@app.route("/cadastro")
def cadastro():
    """Renderiza a página de cadastro do sneaker (formulário)."""
    return render_template("cadastro.html")

# Define a rota que recebe o formulário de cadastro.
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    # Coleta campos do formulário (responsável + sneaker)
    nome_responsavel = request.form.get("nome_responsavel", "").strip()
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()
    sneaker_nome = request.form.get("sneaker_nome", "").strip()
    marca = request.form.get("marca", "").strip()
    modelo = request.form.get("modelo", "").strip()
    tipo = request.form.get("tipo", "").strip()
    tamanho = request.form.get("tamanho", "").strip()
    cor = request.form.get("cor", "").strip()
    observacoes = request.form.get("observacoes", "").strip()

    # Validação mínima
    if not nome_responsavel or not email or not sneaker_nome:
        flash("Preencha nome do responsável, e-mail e nome do sneaker.", "erro")
        return redirect(url_for("cadastro"))

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        sql = ("INSERT INTO cadastros (nome_responsavel, telefone, email, sneaker_nome, marca, modelo, tipo, tamanho, cor, observacoes) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (nome_responsavel, telefone, email, sneaker_nome, marca, modelo, tipo, tamanho, cor, observacoes))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash("Cadastro enviado com sucesso.", "sucesso")
    except Error as erro:
        flash(f"Não foi possível cadastrar: {erro}", "erro")

    return redirect(url_for("index"))

# Executa este bloco apenas quando app.py é iniciado diretamente.
if __name__ == "__main__":
    # Garante que a tabela necessária exista antes de iniciar o servidor.
    criar_tabela_cadastros()
    # Inicia o servidor Flask aceitando conexões encaminhadas pelo Docker.
    app.run(host="0.0.0.0", port=5000, debug=False)
