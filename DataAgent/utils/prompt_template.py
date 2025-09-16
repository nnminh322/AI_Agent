import yaml

with open("./documents/query_sql_message_system.txt", "r", encoding="utf-8") as f:
    query_sql_message_system = f.read()

with open("./configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)
dialect = config["database"]["DIALECT"]


def get_first_query_system_message():
    return query_sql_message_system.replace("{DIALECT}", dialect)
