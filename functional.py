from agents.state import MessageState
from node_and_edge.context_node import context_node
from node_and_edge.sys_msg_node import sys_msg_node
from node_and_edge.assistant_node import assistant_node
from node_and_edge.sql_note import sql_query_node
from node_and_edge.sql_verify_edge import sql_verify_edge
from node_and_edge.show import show
from langgraph.graph import StateGraph, START, END


graph = StateGraph(MessageState)

graph.add_node("context_node", context_node)
graph.add_node("sys_msg_node", sys_msg_node)
graph.add_node("assistant_node", assistant_node)
graph.add_node("sql_query_node", sql_query_node)
graph.add_node("show", show)

graph.add_edge(START, "context_node")
graph.add_edge("context_node", "sys_msg_node")
graph.add_edge("sys_msg_node", "assistant_node")
graph.add_edge("assistant_node", "sql_query_node")
graph.add_conditional_edges("sql_query_node", sql_verify_edge)
graph.add_edge("show", END)

# graph.add_edge("sql_query_node", END)
app = graph.compile()

# question = "Chất lượng vận hành theo quy mô seller: chia seller thành 10 decile theo GMV và báo cáo tỉ lệ hủy đơn (canceled rate) và tỉ lệ giao trễ (delivered muộn so với estimated) của mỗi decile."


def chat_sql(question: str):
    state = MessageState()
    state["question"] = question
    try:
        out_state = app.invoke(state)
    except Exception as e:
        return {"error": str(e)}
    return {"results": out_state["SQL_data_results"]}
