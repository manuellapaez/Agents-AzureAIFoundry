import sqlite3
import requests
from datetime import datetime

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

# Registrar evento de ruptura
def registrar_ruptura(dados):
    inicializar_base()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    produto = dados.get("Produto afetado")
    cliente = dados.get("Nome do cliente")
    loja = dados.get("Nome do PDV")
    endereco = dados.get("Endereço do PDV")
    data = dados.get("Data", datetime.now().isoformat())
    correoeletronico = dados.get("E-mail do gerente da conta")

    cursor.execute("""
    INSERT INTO rupturas (produto, cliente, loja, endereco, data, correoeletronico)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (produto, cliente, loja, endereco, data, correoeletronico))

    conn.commit()
    conn.close()
    return "💾 Ruptura registrada na base de dados."

# Enviar alerta por e-mail
def enviar_alerta_gerente(dados, access_token):
    gerente_email = dados.get("E-mail do gerente da conta")
    if not gerente_email:
        return "⚠️ E-mail do gerente não informado. Alerta não enviado."

    assunto = f"Alerta de ruptura: {dados.get('Produto afetado')}"
    corpo = dados.get("Conteúdo do e-mail para o gerente")
    if not corpo:
        corpo = (
            f"Cliente: {dados.get('Nome do cliente')}\n"
            f"PDV: {dados.get('Nome do PDV')}\n"
            f"Endereço: {dados.get('Endereço do PDV')}\n"
            f"Produto: {dados.get('Produto afetado')}\n\n"
            f"Justificativa: {dados.get('Justificativas', {}).get('Enviar email alerta', 'Não informada')}"
        )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": {
            "subject": assunto,
            "body": {
                "contentType": "Text",
                "content": corpo
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": gerente_email
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=payload
    )

    if response.status_code == 202:
        return "📧 Alerta enviado ao gerente via Graph API."
    else:
        return f"❌ Falha ao enviar e-mail: {response.text}"

# Simular criação de demanda via API para promotor
def criar_demanda_promotor(dados):
    print("\n📦 Simulação: criando demanda via API para o promotor.")
    # dados omitidos por segurança em ambiente de produção
    return "✅ Demanda simulada com sucesso."

# Fim do arquivo actions.py
