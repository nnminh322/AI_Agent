from agents.state import MessageState
from langgraph.graph import StateGraph
from utils.prompt_template import get_first_query_system_message

def context_node(state: MessageState) -> MessageState:
    """Adding history_chat and database_description to state for llm knows context"""
    with open("./documents/database_description.txt", 'r') as f:
        db_des = f.read()
    
    state['db_description'] = db_des
    state['chat_history'] = ""
    state["system_msg"] = get_first_query_system_message()
    return state

# def greeting_node(state: MessageState) -> MessageState:
#     """Start node, adding question input to state"""
    
