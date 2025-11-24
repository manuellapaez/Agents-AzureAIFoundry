import sqlite3
from datetime import datetime, timedelta

DB_PATH = "<your-db-path>.db"

# Inicializa a base de dados se ainda não existir
def inicializar_base():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rupturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            cliente TEXT,
            loja TEXT,
            endereco TEXT,
            data TEXT,
            correoeletronico TEXT
        )
    """)
    conn.commit()
    conn.close()

# Função auxiliar: verificar recorrência
def verificar_recorrencia(produto, cliente, loja):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    limite = datetime.now() - timedelta(days=15)

    cursor.execute("""
        SELECT COUNT(*) FROM rupturas
        WHERE produto = ? AND cliente = ? AND loja = ? AND data >= ?
    """, (produto, cliente, loja, limite.strftime("%Y-%m-%d %H:%M:%S")))

    qtd = cursor.fetchone()[0]
    conn.close()
    return qtd >= 2  # só considera recorrência se houver 2 ou mais registros

# Registrar evento de ruptura
def registrar_ruptura(dados):
    inicializar_base()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    produto = dados.get("Produto afetado")
    cliente = dados.get("Nome do cliente")
    loja = dados.get("Nome do PDV")
    endereco = dados.get("Endereço do PDV")
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Sempre captura a data atual
    correoeletronico = dados.get("E-mail do gerente da conta")

    cursor.execute("""
        INSERT INTO rupturas (produto, cliente, loja, endereco, data, correoeletronico)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (produto, cliente, loja, endereco, data, correoeletronico))

    conn.commit()
    conn.close()

    # Checar recorrência
    if verificar_recorrencia(produto, cliente, loja):
        return f"💾 Ruptura registrada. ⚠️ Recorrência detectada para {produto} no PDV {loja}."
    else:
        return "💾 Ruptura registrada na base de dados."

# Enviar alerta por e-mail (simulação segura)
def enviar_alerta_gerente(dados, access_token=None):
    gerente_email = dados.get("E-mail do gerente da conta")
    if not gerente_email:
        return "⚠️ E-mail do gerente não informado. Alerta não enviado."

    assunto = f"Alerta de ruptura: {dados.get('Produto afetado')}"
    corpo = (
        f"Cliente: {dados.get('Nome do cliente')}\n"
        f"PDV: {dados.get('Nome do PDV')}\n"
        f"Endereço: {dados.get('Endereço do PDV')}\n"
        f"Produto: {dados.get('Produto afetado')}\n\n"
    )

    print("\n📧 Simulação: alerta de ruptura enviado ao gerente.")
    print(f"Destinatário: {gerente_email}")
    print(f"Assunto: {assunto}")
    print(f"Corpo: {corpo}")
    print("✅ Alerta simulado com sucesso.")
    return

# Simular criação de demanda via API para promotor
def criar_demanda_promotor(dados):
    print("\n📦 Simulação: criando demanda via API para o promotor.")
    print(f"Cliente: {dados.get('Nome do cliente')}")
    print(f"PDV: {dados.get('Nome do PDV')}")
    print(f"Produto: {dados.get('Produto afetado')}")
    print(f"Endereço: {dados.get('Endereço do PDV')}")
    print(f"Justificativa: {dados.get('Justificativas', {}).get('Criar demanda via API para promotor', 'Não informada')}")
    print("✅ Demanda simulada com sucesso.")
    return
    
# Fim do arquivo actions.py
