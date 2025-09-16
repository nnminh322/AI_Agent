from agents.state import MessageState
from typing import Literal

def sql_verify_edge(state: MessageState) -> Literal["sys_msg_node", "show"]:
    # Kiểm tra nếu đã vượt quá số lần retry tối đa
    if state["SQL_num_retry"] >= 3:
        return "show"
    
    elif state.get("SQL_error_results") is not None:
        state["SQL_num_retry"] = state["SQL_num_retry"] + 1
        return "sys_msg_node"
    
    else:
        return "show"