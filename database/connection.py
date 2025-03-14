import streamlit as st
import pyodbc
from pyodbc import Connection

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={st.secrets['server']};"
    f"Database={st.secrets['database']};"
    f"Uid={st.secrets['username']};"
    f"Pwd={st.secrets['password']};"
    "Encrypt=no;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

@st.cache_resource
def init_connection() -> Connection:
    return pyodbc.connect(connection_string)


def execute_query(conn, query, results:bool=True):
    with conn.cursor() as cur:
        cur.execute(query)
        if results:
            return cur.fetchall()

def list_tables():
    query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'dbo'
    """
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        return [row[0] for row in cur.fetchall()]
