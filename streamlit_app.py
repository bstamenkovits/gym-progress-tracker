import streamlit as st
from database.table import BaseTable
from database.connection import list_tables

st.write("test")

class MyTable(BaseTable):
    name = 'test'
    schema = {
        "id":"INT",
        "name":"NVARCHAR(200)"
    }

my_table = MyTable()
my_table.drop()
tables = list_tables()
print(tables)





# connection_string = (
#     "Driver={ODBC Driver 18 for SQL Server};"
#     f"Server={st.secrets['server']};"
#     f"Database={st.secrets['database']};"
#     f"Uid={st.secrets['username']};"
#     f"Pwd={st.secrets['password']};"
#     "Encrypt=no;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )

# # Initialize connection.
# # Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():
#     return pyodbc.connect(connection_string)

# conn = init_connection()

# # with conn.cursor() as cur:
# #     cur.execute("CREATE TABLE test (id INT, name NVARCHAR(200))")

# # Perform query.
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# # @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

# rows = run_query("SELECT * FROM test")
# print(rows)

# # Print results.
# for row in rows:
#     st.write(f"{row[0]} has a :{row[1]}:")
#     print(row)
