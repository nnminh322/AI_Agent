from nodes.context_node import context_node
from agents.state import MessageState
from tools.sql_tools import query_sql
def main():
    start_state = MessageState()
    start_state['question'] = "Hello, you are an helpful Data Agent"
    state = context_node(state=start_state)
    print(state)

# def main():
#     print("test sql execute function")
#     query = "SELECT * from olist.olist_customers oc "
#     results = query_sql(sql_statement=query)
#     print((results))


if __name__ == "__main__":
    main()