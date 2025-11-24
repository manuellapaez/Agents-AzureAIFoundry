import time
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder
from actions import registrar_ruptura, enviar_alerta_gerente, criar_demanda_promotor, verificar_recorrencia

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
    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"🚀 Run iniciado: {run.id}")

    if run.status == "failed":
        dados = {
            "status": "alerta incompleto",
            "motivo": f"Run terminou com status {run.last_error}"
        }
        print(f"⚠️ Run não finalizou com sucesso. Retornando alerta incompleto.")
        return dados
        
    # Obter resposta do agente
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    resposta_json = None

    for msg in messages:
        if msg.text_messages:
            texto = msg.text_messages[-1].text.value.strip()

            # Se vier com bloco ```json ... ```
            if texto.startswith("```"):
                inicio = texto.find("\n")
                fim = texto.rfind("```")
                if inicio != -1 and fim != -1:
                    texto = texto[inicio+1:fim].strip()

            # Tentar interpretar como JSON
            try:
                resposta_json = json.loads(texto)
                break  # achou JSON válido, não precisa continuar
            except json.JSONDecodeError:
                continue

    if not resposta_json:
        print("⚠️ Nenhuma resposta JSON válida recebida do agente.")
        return {"status": "alerta incompleto", "motivo": "Agente não retornou JSON"}

    print("\n📦 Resposta do agente (JSON):")
    print(json.dumps(resposta_json, indent=2, ensure_ascii=False))

    # Executar regras de decisão
    print("\n🔧 Ações recomendadas pelo agente:")
    canais = resposta_json.get("Canais de execução", {})

    for acao in resposta_json.get("Ações recomendadas", []):
        canal = canais.get(acao, "Canal desconhecido")
        print(f"- {acao} → {canal}")

    print("\n⚙️ Executando ações:")
    for acao in resposta_json.get("Ações recomendadas", []):
        if acao == "Registrar evento de ruptura":
            registrar_ruptura(resposta_json)
        elif acao == "Criar demanda via API para promotor":
            criar_demanda_promotor(resposta_json)
        elif acao == "Enviar email alerta":
            if verificar_recorrencia(resposta_json["Produto afetado"], resposta_json["Nome do cliente"], resposta_json["Nome do PDV"]):
                enviar_alerta_gerente(resposta_json, access_token)
            else:
                print("Alerta não enviado: sem recorrência registrada.")

    # 🔧 Regra híbrida: alerta disparado pelo código mesmo sem recomendação explícita
    if verificar_recorrencia(
        resposta_json["Produto afetado"],
        resposta_json["Nome do cliente"],
        resposta_json["Nome do PDV"]
    ):
        enviar_alerta_gerente(resposta_json, access_token)

    return resposta_json

# Fim do arquivo agent_client.py
