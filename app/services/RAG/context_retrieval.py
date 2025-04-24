from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from app.utilities.configuration import APP_CONFIG
from app.utilities.logger_util import logger

embedding_model = APP_CONFIG["EMBEDDING_MODEL"]


def get_context(payload):
    """
    Get the context from Azure Search based on the query and index name.
    """
    logger.info("------- invoked get_context() -------")
    # Azure Search Configuration
    endpoint = APP_CONFIG["AZURE_SEARCH_ENDPOINT"]
    admin_key = APP_CONFIG["AZURE_SEARCH_KEY"]
    filter_query = ""

    try:
        # Create the SearchClient
        search_client = SearchClient(endpoint=endpoint, index_name=payload.index_name,
                                     credential=AzureKeyCredential(admin_key))

        if payload.filename:
            filter_query = f"filename eq '{payload.filename}'"

        # Perform a vector search
        results = search_client.search(
            search_text=payload.query,
            top=payload.top_k,
            filter=filter_query
        )

        context_text = ""
        context_list = []
        sources = []

        # Print results
        for result in results:
            context_text += result['chunk']
            context_list.append(result['chunk'])
            #fetch sources for each chunk
            sources.append({
                "filename": result['filename'],
                "score": result['@search.score'],
            })
            print(f"Source: {result['filename']}, Score: {result['@search.score']}")
        logger.info("------- get_context() completed -------")

        return context_text, context_list, sources

    except Exception as e:
        logger.error(f"Error in get_context: {str(e)}")
        return None, None

