from typing import TypedDict, Literal, Dict, List, Any, Optional
from langgraph.graph import StateGraph
class MessageState(TypedDict):
    SQL_format: Literal['postgres', 'mssql', 'mysql']
    question: str
    db_description: str
    chat_history: List[Dict[str,str]]
    SQL_statement: Optional[str]
    SQL_error_results: Optional[str]
    SQL_num_retry: int
    SQL_data_results: Optional[List[Dict[str, Any]]]
