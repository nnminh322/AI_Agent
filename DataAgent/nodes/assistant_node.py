from llm.llm_model import LLM_standard_OpenAI_API
from agents.state import MessageState

llm = LLM_standard_OpenAI_API().get_llm()

def assistant_node(state: MessageState) -> MessageState:
    """This node take an state and return a sql_statement"""
    user_prompt = f"""
    Database Dialect: postgres
    Database Schema:
    {state['db_description']}

    User Question: {state['question']}

    Generate SQL query:
    """
    
    messages = [
        {"role": "system", "content": state["system_msg"]},
        {"role": "user", "content": user_prompt}
    ]
    
    response = llm.invoke(input = messages)
    raw_sql = response.content.strip()
    cleaned_sql = raw_sql.replace('```sql\n', '').strip().replace('```', '')
    
    state["SQL_statement"] = cleaned_sql
    return state
    