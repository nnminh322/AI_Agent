from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
import os

# os.environ["LANGSMITH_API_KEY"] = "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"

# Tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# LLM with bound tool
llm = llm = ChatOpenAI(
    model="openai/gpt-4o",
    api_key="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",
    base_url="https://models.github.ai/inference",
)
llm_with_tools = llm.bind_tools([multiply])

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)

# Compile graph
graph = builder.compile()