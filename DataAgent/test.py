from nodes.context_node import context_node
from agents.state import MessageState
from tools.sql_tools import query_sql
from llm.llm_model import LLM_standard_OpenAI_API
from utils.prompt_template import get_first_query_system_message
# def main():
#     start_state = MessageState()
#     start_state['question'] = "Hello, you are an helpful Data Agent"
#     state = context_node(state=start_state)
#     print(state)

def main():
    llm = LLM_standard_OpenAI_API().get_llm()
    input = "Hello, Do you known HUST?"
    output = llm.invoke(input=input)
    print(output)

# def main():
#     sys_msg = get_first_query_system_message()
#     print(sys_msg)

# def main():
#     print("test sql execute function")
#     query = "SELECT * from olist.olist_customers oc "
#     results = query_sql(sql_statement=query)
#     print((results))


if __name__ == "__main__":
    main()