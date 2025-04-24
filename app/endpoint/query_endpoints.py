from fastapi import APIRouter, Request, Depends

from app.model.query_models import QueryParameters, parse_query_param, QueryResponseModel
from app.services.llm_service import QueryHandler
from app.services.RAG.context_retrieval import get_context
from app.services.ragas_evaluation_service import evaluate_metrics
from app.utilities.logger_util import logger

router = APIRouter()
QueryObj = QueryHandler()


@router.post("/query", response_model=QueryResponseModel)
async def query(request: Request, payload: QueryParameters = Depends(parse_query_param)):
    """
    Endpoint to query on the document
    """
    logger.info("------- invoked query() -------")
    logger.info(f"Payload: {payload}")
    evaluation_result = {}
    context_text, context_list, sources_list = get_context(payload)
    processed_llm_answer = QueryObj.get_answer(payload=payload, context=context_text)

    # Call the evaluation function if enable_evaluation is True
    if payload.enable_evaluation:
        evaluation_result = evaluate_metrics(payload=payload, context=context_list, llm_response=processed_llm_answer)
        evaluation_result['Context'] = context_list

    logger.info("------- query() completed -------")
    return QueryResponseModel(question=payload.query, answer=processed_llm_answer,
                              sources=sources_list, evaluation_results=evaluation_result)
