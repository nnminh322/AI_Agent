from langgraph.graph import StateGraph
from state import MessageState
from tools.sql_tools import sql_query_tool, sql_verify_tool
from tools.analysis_tool import analysis_data_tool
from tools.viz_tool import show_data_tool, show_visualize_tool

class DataAgent:
    def __init__(self):
        builder = StateGraph(MessageState)
        builder.add_node("gen_sql", gen_sql)
        builder.add_node("run_sql", run_sql)
        builder.add_node("verify", verify)
        builder.add_node("analyze", analyze)
        builder.add_node("show", show)

        builder.add_edge(START, "gen_sql")
        builder.add_edge("gen_sql", "run_sql")
        builder.add_edge("run_sql", "verify")
        builder.add_conditional_edges("verify", should_continue, {"gen_sql": "gen_sql", "analyze": "analyze"})
        builder.add_edge("analyze", "show")
        builder.add_edge("show", END)

        self.graph = builder.compile()

    def invoke(self, question: str):
        return self.graph.invoke({"question": question, "messages": []})