import fitz  # PyMuPDF para extrair texto de PDFs
import pyodbc
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (SimpleField, SearchIndex, SearchFieldDataType)
from azure.storage.blob import BlobServiceClient
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Configuração do Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING = "sua_conexao_blob"
BLOB_CONTAINER_NAME = "pdfs"
storage_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
blob_container = storage_client.get_container_client(BLOB_CONTAINER_NAME)

# Configuração do Azure SQL Database
SQL_CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=seu_servidor;DATABASE=sua_base;UID=seu_usuario;PWD=sua_senha"

# Configuração do Azure AI Text Analytics
AZURE_AI_ENDPOINT = "seu_endpoint_azure_ai"
AZURE_AI_KEY = "sua_chave_azure_ai"
text_analytics_client = TextAnalyticsClient(endpoint=AZURE_AI_ENDPOINT, credential=AzureKeyCredential(AZURE_AI_KEY))

# Configuração do Azure Cognitive Search
AZURE_SEARCH_SERVICE_NAME = "seu_servico_search"
AZURE_SEARCH_ADMIN_KEY = "sua_chave_search"
AZURE_SEARCH_INDEX_NAME = "documentos"
search_client = SearchClient(endpoint=f"https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net/",
                             index_name=AZURE_SEARCH_INDEX_NAME, credential=AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY))
index_client = SearchIndexClient(endpoint=f"https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net/",
                                 credential=AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY))


def create_search_index():
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="nome", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="texto", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="sentimento", type=SearchFieldDataType.String, filterable=True)
    ]
    index = SearchIndex(name=AZURE_SEARCH_INDEX_NAME, fields=fields)
    index_client.create_or_update_index(index)


def store_pdf_in_blob(file: UploadFile):
    blob_client = blob_container.get_blob_client(file.filename)
    blob_client.upload_blob(file.file.read(), overwrite=True)
    return blob_client.url


def extract_text_from_pdf(file: UploadFile):
    text = ""
    with fitz.open(stream=file.file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def analyze_text_with_ai(text: str):
    documents = [text]
    response = text_analytics_client.analyze_sentiment(documents=documents)
    return response[0].sentiment


def save_text_to_db(filename: str, text: str, sentiment: str):
    conn = pyodbc.connect(SQL_CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Documentos (nome, texto, sentimento) VALUES (?, ?, ?)", (filename, text, sentiment))
    conn.commit()
    conn.close()


def index_document_in_search(filename: str, text: str, sentiment: str):
    document = {"id": filename, "nome": filename, "texto": text, "sentimento": sentiment}
    search_client.upload_documents(documents=[document])


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_url = store_pdf_in_blob(file)
    extracted_text = extract_text_from_pdf(file)
    sentiment = analyze_text_with_ai(extracted_text)
    save_text_to_db(file.filename, extracted_text, sentiment)
    index_document_in_search(file.filename, extracted_text, sentiment)
    return {"message": "Arquivo enviado e processado com sucesso", "pdf_url": pdf_url}


@app.get("/search/")
def search(query: str):
    results = search_client.search(query)
    return {"results": [doc for doc in results]}
