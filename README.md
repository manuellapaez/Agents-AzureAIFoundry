# Agents-AzureAIFoundry
Intelligent agent framework built on Microsoft Azure AI Foundry. This repository hosts the *rupturapdv* project, featuring a single active agent designed to detect and respond to product stockouts in retail locations by parsing emails, extracting structured data, and triggering automated actions.

## Features
- **AI-Powered Email Parsing:** Uses the agent to extract rupture data from unstructured email content.
- **Structured JSON Output:** Agent returns a consistent schema with fields like PDV, product, client, and recommended actions.
- **Automated Action Execution:** Executes actions such as database logging, email alerts, and API calls based on agent output.
- **Microsoft Graph Integration:** Secure email reading and dispatch using OAuth2 and Graph API.
- **SQLite Persistence:** Local database stores rupture events for audit and analysis.
- **API Simulation (placeholder):** Demand creation is currently mocked for testing purposes until the real API is available.

## Installation
### Dependencies and Foundations

This project builds on the following technologies and requirements:

- **Python 3.11+**: Core language for agent logic and orchestration
- **Microsoft Graph API**: Secure email access, dispatch, and event handling
- **Azure AI Foundry**: Agent orchestration and knowledge integration (agent: *rupturapdv*)
- **SQLite**: Lightweight local persistence (included by default)
- **Microsoft 365 account**: Required for Graph API access
- **RESTful API principles**: Used for future demand integration

### Setup
This repository assumes familiarity with Python environments, Azure AI Foundry, and Microsoft Graph. For this reason, no installation instructions are provided.
All required dependencies are declared within the source files, and all relevant information about the solution is documented below.

### Development Environment
This project was developed and tested using:
- Visual Studio Code (v1.106.0)
- Python 3.14.0
- Azure AI Foundry (via web interface)
- Microsoft Graph API (via registered Azure application)

All scripts were executed locally using VS Code's integrated terminal and debugger.

## Usage
### 1. Configure Microsoft Graph Autentication
Set up OAuth2 credentials and ensure the following scopes are granted:

``Mail.ReadWrite``


### 2. Run the Email Reader
⚠️ Replace YOUR_CLIENT_ID, YOUR_TENANT_ID, and YOUR_FOLDER_ID with your actual credentials before running.

```email_reader.py```


This will read incoming emails, extract content, mark as read, and forward to the rupturapdv agent.
> 📂 Note: The agent is configured to read emails exclusively from a dedicated folder named **Rupturas**.  
> This folder should contain only stockout-related messages to ensure accurate parsing and action triggering.  
> Emails outside this context may lead to irrelevant or failed agent responses.

### 3. Agent Response and Action Execution
The agent returns a structured JSON like:

```
{
  "Nome do PDV": "Supermercado Central",
  "Produto afetado": "Leite Integral",
  "Nome do cliente": "Cliente XYZ",
  "E-mail do gerente da conta": "gerente@xyz.com",
  "Conteúdo do e-mail para o gerente": "Olá, identificamos ruptura...",
  "Ações recomendadas": ["Registrar evento de ruptura", "Enviar email alerta"]
}
```

The system then:
- Logs the event in ``dados_ruptura.db``
  
- Sends an alert email via Microsoft Graph in case of recurring events
- Simulates an API demand creation for clients with automatic stockout replenishment service

## Agent Configuration: rupturapdv (Azure AI Foundry)
### Objective
Interpret emails reporting product stockouts at retail points of sale and recommend corrective actions based on business rules and context.

### LLM Model

``gpt.4o.mini (version: 2024/07/18)``

### Configuration Note

> ⚠️ Replace `<your-resource-name>`, `<your-project-name>`, and `<your-agent-id>` in `agent_client.py` with your actual Azure AI Foundry configuration before running.

### Knowledge Sources
- List of clients with automatic stockout replenishment service
- List of point-of-sale (PoS) addresses
- List of account managers' emails for proactive contact in case of recurring events
- Example instruction for expected JSON output
- Business rules and operational guidelines

### System Instructions
The agent is instructed to:
- Extract fields such as PoS name, product, client, and stockout occurrence
- Return structured JSON with recommended actions
- Justify each action and specify the execution channel
- Prioritize actions based on client data and business rules

### Validation
Tested with:
- AI Playgrounds
- Short, direct emails
- Informal language
- Multiple products affected
- Clients with and without replenishment service

## Visual Schema
This diagram illustrates the end-to-end flow of the rupturapdv agent, from email ingestion to action execution:
- **Email Received** → via Microsoft Graph API
- **Email Parsed** → agent extracts structured data
- **Agent Response** → JSON with recommended actions
- **Action Execution** → database logging, email alerts, API simulation
- **Persistence & Audit** → rupture events stored in SQLite

See diagram below for a visual overview of the system architecture.

## Screenshots

**1. Agent setup (instructions, description and knowledge source)**

**2. Agent response with structured JSON**

**3. Stockout event logged in SQLite**

**4. Email alert sent via Microsoft Graph**


## Security and Permissions
OAuth2 Scopes
- Mail.ReadWrite: Read and send emails, and mark them as read
- Mail.Send: Send alert emails on behalf of the user

## Network and APIs
- All external communication occurs over port 443 (HTTPS)
- Integrates with:
  - Microsoft Graph API
  - Azure AI Foundry API
  - (Planned) Promotor API
- No local ports are exposed
- The agent runs as a local script and communicates exclusively with external APIs over HTTPS
- All communication is encrypted and authenticated

## Dependencies
- azure-ai-projects: Azure AI Foundry SDK
- msal: Microsoft Authentication Library
- requests: HTTP client for API simulation
- sqlite3: Local database engine
- email.message: Email formatting
- smtplib: (fallback, not used with Graph)
- json: JSON parsing and formatting
- logging: Application logging
- datetime: Timestamping events
- time: Delay handling
- re: Regular expressions for parsing

## Mapped Improvements
The following enhancements have been identified for future iterations:

- **Dynamic Folder Detection**: Replace hardcoded folder ID with automatic lookup by name or metadata.
- **Environment Variable Support**: Move sensitive credentials and configuration to `.env` files for better security.
- **Error Handling**: Improve resilience against malformed emails, empty fields, or failed API responses.
- **Multi-Agent Support**: Extend architecture to support multiple agents for different business contexts.
- **Dashboard Integration**: Visualize rupture events and agent responses in a web-based dashboard.
- **Real API Integration**: Replace simulated demand creation with live integration to the Promotor API.
- **Unit Tests**: Add automated tests for email parsing, agent communication, and action execution.
  
## Acknowledgements
- Built on Microsoft Azure AI Foundry
- Utilizes Microsoft Graph API for email handling
- Inspired by real-world retail stockout management challenges

## Disclaimer
This project is for educational and demonstration purposes only. It is not intended for production use without further development, testing, and security review.

## Contributions and contact
Contributions are welcome! Please open issues or pull requests for bug fixes, enhancements, or new features.

For questions or support, please contact me.

**Manuella Paez**
