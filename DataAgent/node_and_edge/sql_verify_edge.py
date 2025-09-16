from agents.state import MessageState
from langgraph.graph import END
from typing import Literal

def sql_verify(state: MessageState) -> MessageState:
    if state["SQL_num_retry"] == 3:
        pass