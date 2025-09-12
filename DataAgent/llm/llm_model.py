from langchain_openai import ChatOpenAI


class LLM_standard_OpenAI_API:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="openai/gpt-4o",
            api_key="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",
            base_url="https://models.github.ai/inference",
        )
    def get_llm(self):
        return self.llm
    

def main():
    llm = LLM_standard_OpenAI_API().get_llm()
    input = "Hello, Do you known HUST?"
    output = llm.invoke(input=input)
    print(output)

if __name__ == "__main__":
    main()

    


