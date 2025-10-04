from langchain_openai import ChatOpenAI
import yaml
import os

# with open("./configs/config.yaml", "r") as file:
#     config = yaml.safe_load(file)
# config_llm = config["llm"]


class LLM_standard_OpenAI_API:
    def __init__(self):

        self.config_api_openai = self._get_config()
        self.llm = ChatOpenAI(**self.config_api_openai)

    def get_llm(self):
        return self.llm

    def _get_config(self):
        API_KEY = os.environ.get("API_KEY")
        MODEL_NAME = os.environ.get("MODEL_NAME")
        BASE_URL = os.environ.get("BASE_URL")

        return {"model": MODEL_NAME, "api_key": API_KEY, "base_url": BASE_URL}
