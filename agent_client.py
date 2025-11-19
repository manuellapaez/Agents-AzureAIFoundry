import time
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder
from actions import registrar_ruptura, enviar_alerta_gerente, criar_demanda_promotor

# Conectar ao projeto da Fábrica de IA (substitua pelo end point real)
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://<your-resource-name>.services.ai.azure.com/api/projects/<your-project-name>"
)

# Obter o agente (substitua pelo seu ID real)
agent_id = "<your-agent-id>"
agent = project.agents.get_agent(agent_id)

# Função principal para processar o e-mail
def enviar_para_agente(assunto: str, corpo: str, remetente: str = None, access_token: str = None):
    texto_email = f"Assunto: {assunto}\nRemetente: {remetente}\n\n{corpo}"

    # Criar thread
    thread = project.agents.threads.create()
    print(f"🧵 Thread criada: {thread.id}")

    # Enviar mensagem
    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=texto_email
    )
    print("✉️ Mensagem enviada ao agente.")

    # Criar e processar run
    run = project.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"🚀 Run iniciado: {run.id}")

    # Aguardar finalização
    while run.status in ["queued", "in_progress"]:
        time.sleep(1)
        run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)

    # Obter resposta
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    resposta = None
    for msg in messages:
        if msg.text_messages:
            resposta = msg.text_messages[-1].text.value

    if not resposta:
        print("⚠️ Nenhuma resposta recebida do agente.")
        return None

    print("\n📦 Resposta do agente:")
    print(resposta)

    # Tentar interpretar como JSON
    try:
        dados = json.loads(resposta)
    except json.JSONDecodeError:
        print("❌ Resposta não está em formato JSON estruturado.")
        return resposta

    # Executar ações recomendadas
    acoes = dados.get("Ações recomendadas", [])
    print("\n🔧 Executando ações:")
    for acao in acoes:
        if acao == "Registrar evento de ruptura":
            print(registrar_ruptura(dados))
        elif acao == "Enviar email alerta":
            print(enviar_alerta_gerente(dados, access_token))
        elif acao == "Criar demanda via API para promotor":
            print(criar_demanda_promotor(dados))
        else:
            print(f"⚠️ Ação não reconhecida: {acao}")

    return resposta


#Fim do arquivo agent_client.py
