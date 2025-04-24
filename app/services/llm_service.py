from app.services.anthropic_claude_service import Anthropic
from app.services.openai_service import OpenAI
from app.utilities.logger_util import logger

AnthropicObj = Anthropic()
OpenAIObj = OpenAI()


class QueryHandler:
    def get_answer(self, payload, context=None) -> str:
        logger.info("------- invoked get_answer() -------")

        if AnthropicObj.match_model(payload.llm_type):
            answer = AnthropicObj.get_answer(payload, context=context)
        elif OpenAIObj.match_model(payload.llm_type):
            answer = OpenAIObj.get_answer(payload, context=context)

        else:
            logger.error(f"Unsupported LLM type: {payload.llm_type}")
            raise ValueError(f"Unsupported LLM type: {payload.llm_type}")

        logger.info("------- get_answer() completed -------")

        return answer
