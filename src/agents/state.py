from typing import TypedDict, Literal, Dict, List, Any, Optional, NotRequired
from langgraph.graph import StateGraph

class SQLError(TypedDict, total=False):
    type: str                 
    message: str              
    code: NotRequired[str]    
    detail: NotRequired[str]  
    retryable: NotRequired[bool]

class MessageState(TypedDict):
    SQL_format: Literal['postgres', 'mssql', 'mysql']
    question: str
    system_msg: Optional[str]
    db_description: str
    chat_history: List[Dict[str,str]]
    SQL_statement: Optional[str]
    SQL_error_results: Optional[str]
    SQL_num_retry: int
    SQL_data_results: Optional[List[Dict[str, Any]]]
