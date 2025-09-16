from llm.llm_model import LLM_standard_OpenAI_API
from agents.state import MessageState

llm = LLM_standard_OpenAI_API().get_llm()


def assistant_node(state: MessageState) -> MessageState:
    """This node take an state and return a sql_statement"""
    sys_msg = state["system_msg"]
    user_msg = f"""
    Database Dialect: {state["SQL_format"]}
    Database Schema:
    {state['db_description']}

    User Question: {state['question']}

    Generate SQL query:
    """

    messages = [
        {"role": "system", "content": state["system_msg"]},
        {"role": "user", "content": user_msg},
    ]

    response = llm.invoke(input=messages)
    raw_sql = response.content.strip()
    if raw_sql.startswith("```sql"):
        cleaned_sql = raw_sql[6:]  
        if cleaned_sql.endswith("```"):
            cleaned_sql = cleaned_sql[:-3]
    elif raw_sql.startswith("```"):
        cleaned_sql = raw_sql[3:]
        if cleaned_sql.endswith("```"):
            cleaned_sql = cleaned_sql[:-3]
    else:
        cleaned_sql = raw_sql

    state["SQL_statement"] = cleaned_sql.strip()
    return state
