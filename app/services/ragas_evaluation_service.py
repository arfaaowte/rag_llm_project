from ragas.metrics import ContextRelevance, AnswerRelevancy, Faithfulness, \
    AnswerCorrectness, AnswerSimilarity
from ragas.evaluation import EvaluationResult
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas import SingleTurnSample
from typing import List

from app.utilities.configuration import APP_CONFIG
from app.utilities.logger_util import logger

evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=APP_CONFIG["openai_model"], api_key=APP_CONFIG["OPENAI_API_KEY"]))
similarity_model = AnswerSimilarity()


def evaluate_metrics(payload, context: List[str], llm_response: str) -> dict:
    """
    Evaluate the metrics for the given payload, context, and LLM response.
    """
    logger.info("------- invoked evaluate_metrics() -------")

    try:
        record = {
            'user_input': payload.query,
            'retrieved_contexts': context,
            'response': llm_response,
            'reference': payload.expected_answer if payload.expected_answer else None
        }

        test_data = SingleTurnSample(**record)

        # Evaluate metrics
        results = {"Context Relevance": ContextRelevance(llm=evaluator_llm).single_turn_score(test_data),
                   "Answer Relevancy": AnswerRelevancy(llm=evaluator_llm, embeddings=OpenAIEmbeddings(
                       api_key=APP_CONFIG["OPENAI_API_KEY"])).single_turn_score(
                       test_data),
                   "Faithfulness": Faithfulness(llm=evaluator_llm).single_turn_score(test_data)}

        # Optional metric: Answer Correctness
        if record["reference"]:
            answer_correctness = AnswerCorrectness(llm=evaluator_llm, embeddings=OpenAIEmbeddings(api_key=APP_CONFIG["OPENAI_API_KEY"]))
            answer_correctness.answer_similarity = similarity_model
            results["Answer Correctness"] = answer_correctness.single_turn_score(test_data)

        logger.info("------- evaluate_metrics() completed -------")

        return {k: (v.score if isinstance(v, EvaluationResult) else v) for k, v in results.items()}

    except Exception as e:
        logger.error(f"Error in evaluate_metrics: {str(e)}")
        return {"error": str(e)}
