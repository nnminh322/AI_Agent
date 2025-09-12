import psycopg2
import yaml
from typing import Optional, Tuple

with open("../configs/config.yaml", "r") as f:
    postgres_config = yaml.safe_load(f)
conn_params = postgres_config["postgres_config"]


def get_connection_and_cursor() -> (
    Optional[Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]]
):
    try:
        connection = psycopg2.connect(**conn_params)
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Error connection: {e}")
        return None, None


def query_sql(sql_statement: str, commit: bool = False):
    connection, cursor = get_connection_and_cursor()
    if not cursor:
        return None
    try:
        cursor.execute(sql_statement)
        if cursor.description:
            rows = cursor.fetchall()
        else:
            rows = None

        if commit:
            connection.commit()
        return rows
    except Exception as e:
        print(f"Error executing SQL: {e}")
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# def main():
#     print("test sql execute function")
#     query = "SELECT * from olist.olist_customers oc "
#     results = query_sql(sql_statement=query)
#     print(type(results))

# if __name__ == "__main__":
#     main()