from langchain_openai import ChatOpenAI
import yaml

with open("./configs/config.yaml", "r") as file:
    config = yaml.safe_load(file)
config_llm = config["llm"]


class LLM_standard_OpenAI_API:
    def __init__(self):
        self.config_api_openai = config_llm["openai"]
        self.llm = ChatOpenAI(**self.config_api_openai)

    def get_llm(self):
        return self.llm
