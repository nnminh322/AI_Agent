import psycopg2
import yaml
from typing import Optional, Tuple
from agents.state import MessageState

with open("./configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)
conn_params = config["postgres_config"]


def get_connection_and_cursor() -> (
    Optional[Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]]
):
    try:
        connection = psycopg2.connect(**conn_params)
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Error connection: {e}")
        return e, None


def query_sql(sql_statement: str, commit: bool = False):
    connection, cursor = get_connection_and_cursor()
    headers = []
    rows = []
    if not cursor:
        return connection
    try:
        cursor.execute(sql_statement)
        if cursor.description:
            headers = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
        else:
            rows = None

        if commit:
            connection.commit()
        return {"headers": headers, "rows": rows}
    except Exception as e:
        print(f"Error executing SQL: {e}")
        connection.rollback()
        return e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def sql_query_tool(state: MessageState) -> MessageState:
    pass


def sql_verify_tool(state: MessageState) -> MessageState:
    pass
