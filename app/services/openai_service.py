import openai

from app.utilities import constants
from app.utilities.configuration import APP_CONFIG
from app.utilities.logger_util import logger

client = openai.Client(
    api_key=APP_CONFIG["OPENAI_API_KEY"]
)


class OpenAI:
    def match_model(self, model_name: str) -> str:
        """
        Check if the model name is supported by OpenAI.
        """
        if model_name in constants.OPENAI_MODELS:
            return model_name

    def get_answer(self, payload, context):
        """
        Get the answer from the OpenAI.
        """
        logger.info("------- invoked get_answer_openai() -------")
        prompt = f"{constants.prompt_with_context}\n Context: {context}\n\nQuestion: {payload.query}"

        # write prompt to file
        with open("prompt.txt", "w") as f:
            f.write(prompt)

        try:
            response = client.responses.create(
                model=APP_CONFIG["OPENAI_MODEL"],
                input=prompt,
                max_output_tokens=payload.max_tokens,
                temperature=payload.temperature,
                top_p=payload.top_p
            )

            logger.info("------- get_answer_openai() completed -------")

            return response.output_text

        except Exception as e:
            return f"Error from OpenAI API: {str(e)}"
