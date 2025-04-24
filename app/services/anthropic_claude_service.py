import anthropic

from app.utilities import constants
from app.utilities.configuration import APP_CONFIG
from app.utilities.logger_util import logger


class Anthropic:
    def match_model(self, model_name: str) -> str:
        """
        Check if the model name is supported by Anthropic Claude API.
        """
        if model_name in constants.ANTHROPIC_MODELS:
            return model_name

    def get_answer(self, payload, context) -> str:
        """
        Get the answer from the Anthropic Claude.
        """
        logger.info("------- invoked get_answer_anthropic() -------")
        prompt = f"{constants.prompt_with_context}\n Context: {context}\n\nQuestion: {payload.query}"

        try:
            client = anthropic.Anthropic(api_key=APP_CONFIG["ANTHROPIC_API_KEY"])

            message = client.messages.create(
                model=APP_CONFIG["ANTHROPIC_MODEL"],
                max_tokens=payload.max_tokens,
                temperature=payload.temperature,
                top_p=payload.top_p,
                system="You are helper",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            logger.info("------- get_answer_anthropic() completed -------")

            return message.content[0].text

        except Exception as e:
            return f"Error from Anthropic Claude API: {str(e)}"
