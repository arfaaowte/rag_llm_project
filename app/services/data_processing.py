from sentence_transformers import SentenceTransformer
import json
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchFieldDataType, VectorSearch,
    VectorSearchProfile, HnswAlgorithmConfiguration, SearchableField, SearchField
)
from azure.core.credentials import AzureKeyCredential

from app.utilities.configuration import APP_CONFIG
from app.utilities.logger_util import logger

embedding_model = APP_CONFIG["EMBEDDING_MODEL"]
embedder = SentenceTransformer(embedding_model)


# Function to process the uploaded JSON file
def process_data(file):
    logger.info("------- invoked process_data() -------")
    content = file.file.read().decode("utf-8")
    data = json.loads(content)
    docs = []
    index_name = file.filename.split(".")[0]

    endpoint = APP_CONFIG["AZURE_SEARCH_ENDPOINT"]
    admin_key = APP_CONFIG["AZURE_SEARCH_KEY"]

    # Step 1: Create index if it doesn't exist
    create_index(admin_key, endpoint, index_name)

    # Step 2: Generate documents with embeddings
    for idx, item in enumerate(data):
        uid = item.get("uid", f"item-{idx}")
        filename = item.get("filename", f"file-{idx}")
        chunk = json.dumps(item)
        embedding = embedder.encode(chunk).tolist()

        docs.append({
            "id": uid,
            "chunk": chunk,
            "embedding": embedding,
            "uid": uid,
            "filename": filename
        })

    try:
        logger.info(f"Uploading {len(docs)} chunks to Azure AI Search...")

        # Step 3: Upload documents via SearchClient
        search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(admin_key))
        result = search_client.upload_documents(documents=docs)

    except Exception as e:
        logger.error(f"Error uploading documents: {e}")
        return f"Error uploading documents: {e}"

    logger.info(f"Uploaded {len(docs)} chunks to Azure AI Search.")
    logger.info("------- process_data() completed -------")

    return f"Uploaded {len(docs)} chunks to Azure AI Search."


def create_index(admin_key, endpoint, index_name):
    logger.info("------- invoked create_index() -------")
    index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(admin_key))
    index = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="chunk", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
            SimpleField(name="uid", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="filename", type=SearchFieldDataType.String, filterable=True),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                vector_search_dimensions=384,
                vector_search_profile_name="default"
            )
        ],
        vector_search=VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(name="default", kind="hnsw")
            ],
            profiles=[
                VectorSearchProfile(name="default", algorithm_configuration_name="default")
            ]
        )
    )
    index_client.create_or_update_index(index)
    logger.info(f"Index {index_name} created or updated.")
    logger.info("------- create_index() completed -------")

