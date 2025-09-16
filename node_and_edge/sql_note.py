from tools.sql_tools import query_sql
from agents.state import MessageState

def sql_query_node(state: MessageState) -> MessageState:
    sql_statement = state.get("SQL_statement")
    if not sql_statement:
        state["SQL_error_results"] = "Missing SQL statement"
    result_query = query_sql(sql_statement=sql_statement)
    
    if isinstance(result_query, Exception):
        state["SQL_error_results"] = str(result_query)
    else:
        state["SQL_data_results"] = result_query
        
    return state

