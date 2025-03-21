# 📌 Azure PDF AI Search

Este projeto implementa um sistema inteligente de busca para documentos PDF, utilizando **Azure AI** para extração de texto e análise de sentimentos, além de **Azure SQL Database** e **Azure Cognitive Search** para indexação e recuperação eficiente de informações.

## 🚀 Funcionalidades
- 📄 **Upload de PDFs**: Armazena arquivos no **Azure Blob Storage**.
- 🔍 **Extração de Texto**: Utiliza **PyMuPDF** para ler PDFs.
- 🤖 **Análise de Sentimentos**: Usa **Azure AI Text Analytics**.
- 📊 **Banco de Dados SQL**: Armazena documentos e metadados.
- 🏎 **Azure Cognitive Search**: Para buscas eficientes e rápidas.
- 📡 **API FastAPI**: Interface para upload e pesquisa de documentos.

## 🛠 Tecnologias Utilizadas
- **Python** + **FastAPI**
- **Azure Blob Storage** (para armazenar PDFs)
- **Azure SQL Database** (para persistência dos dados)
- **Azure AI Text Analytics** (para análise de texto e sentimentos)
- **Azure Cognitive Search** (para indexação e recuperação de informações)

## 📦 Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/azure-pdf-ai-search.git
   cd azure-pdf-ai-search
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. Configure as credenciais do Azure nos arquivos de ambiente.

## 🚀 Como Executar
1. Inicie a API FastAPI:
   ```bash
   uvicorn main:app --reload
   ```
2. Acesse a documentação interativa:
   ```
   http://127.0.0.1:8000/docs
   ```

## 📡 Endpoints da API
- `POST /upload_pdf/` → Faz upload de um PDF e processa seu conteúdo.
- `GET /search/?query=palavra` → Busca documentos indexados.

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se livre para contribuir!

---
💡 **Dúvidas ou sugestões?** Abra uma issue no repositório! 😊

