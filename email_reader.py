from msal import PublicClientApplication
import requests
from agent_client import enviar_para_agente  # integração com o agente

# Configurações do app registrado
CLIENT_ID = "<your-client-id>" # Inserir seu Client_ID
TENANT_ID = "<your-tenant-id>" # Inserir seu Tenent_ID
AUTHORITY = "https://login.microsoftonline.com/consumers" # ou "organizations" se for corporativo
SCOPES = ["Mail.ReadWrite"]  # write necessário para marcar como lido

# Autenticação interativa
app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
result = app.acquire_token_interactive(scopes=SCOPES)

if "access_token" not in result:
    print("❌ Falha na autenticação.")
    exit()

access_token = result["access_token"] # use_your_access_token

# Cabeçalhos para requisições
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# ID fixo da pasta "Rupturas" (substitua pelo seu valor real)

ruptura_folder_id = "YOUR_FOLDER_ID"

# Buscar mensagens não lidas da pasta
messages_url = (
    f"https://graph.microsoft.com/v1.0/me/mailFolders/{ruptura_folder_id}/messages"
    f"?$filter=isRead eq false"
)
emails = requests.get(messages_url, headers=headers).json()

if "value" not in emails:
    print("❌ Erro ao buscar e-mails:", emails)
    exit()

# Paginação para garantir que todos os e-mails sejam processados
while True:
    for item in emails.get("value", []):
        assunto = item.get("subject", "(sem assunto)")
        corpo = item.get("bodyPreview", "(sem corpo)")
        remetente = item.get("from", {}).get("emailAddress", {}).get("address", "(remetente desconhecido)")

        print("📨 Assunto:", assunto)
        print("📝 Corpo:", corpo)
        print("-" * 40)

        # Enviar para o agente
        resultado = enviar_para_agente(assunto, corpo, remetente, access_token)

        # Marcar como lido
        email_id = item["id"]
        patch_url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}"
        requests.patch(patch_url, headers=headers, json={"isRead": True})
        print(f"✅ E-mail {email_id} marcado como lido.\n")

    next_link = emails.get("@odata.nextLink")
    if not next_link:
        break
    emails = requests.get(next_link, headers=headers).json()

    #Fim do arquivo email_reader.py
