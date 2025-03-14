import pandas as pd
from database.connection import init_connection, execute_query, execute_many_query
from typing import List, Dict, Any


class SchemaError(Exception):
    pass


class BaseTable:
    name = ""
    schema = {}

    def __init__(self):
        self.conn = init_connection()
        if self._table_exists():
            self._validate_schema()
        else:
            self._create_table()

    def _table_exists(self) -> bool:
        query = f"""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = '{self.name}'
        """
        rows = execute_query(conn=self.conn, query=query, results=True)

        if rows[0][0] == 1:
            return True
        return False

    def _validate_schema(self) -> None:
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = '{self.name}'
        """
        rows = execute_query(conn=self.conn, query=query, results=True)
        sql_server_schema = {column_name:data_type for column_name, data_type in rows}

        if not sql_server_schema.keys() == self.schema.keys():
            raise SchemaError(
                f"Columns in schema definition of table '{self.name}' do not match those found in SQL Server database."
                f"Found {self.schema.keys()}, expected {sql_server_schema.keys()}")

        for column, data_type in self.schema.items():
            defined_data_type = data_type.lower().split('(')[0]
            expected_data_type = sql_server_schema[column].lower().split('(')[0]

            if defined_data_type != expected_data_type:
                raise SchemaError(
                    f"Incorrect datatype found for column {column} in table {self.name}."
                    f"Expected {expected_data_type}, found {defined_data_type}"
                )

    def _create_table(self) -> None:
        column_definitions = [f"{column} {data_type}" for column, data_type in self.schema.items()]
        column_definitions = ", ".join(column_definitions)

        query = f"CREATE TABLE {self.name} ({column_definitions})"
        execute_query(conn=self.conn, query=query, results=False)

    def drop(self):
        query = f"DROP TABLE {self.name}"
        execute_query(conn=self.conn, query=query, results=False)

    # def insert(self, columns, values)->None:
    #     query = f""""
    #         INSERT INTO {self.name} ({columns})
    #         VALUES ({", ".join(["?" for _ in len(values)])})
    #     """
    #     execute_many_query(conn=self.conn, query=query, data=values)

    def insert(self, data):
        columns, values = [], []
        for column, value in data.items():
            columns.append(column)
            values.append(value)

        query = f"""
            INSERT INTO {self.name} ({", ".join(columns)})
            VALUES ({", ".join(["?" for _ in range(len(values))])})
        """
        execute_many_query(conn=self.conn, query=query, data=(values,))

    def df(self, columns:List[str]=None, conditions:Dict[str, str]=None) -> pd.DataFrame:
        columns = ", ".join(columns) if columns else "*"

        if conditions:
            values = list(conditions.values())
            conditions = [f"{column} = ?" for column in conditions.keys()]
            conditions = " AND ".join(conditions)
        else:
            values = None
            conditions = ""

        query = f"SELECT {columns} FROM {self.name} WHERE 1=1 {conditions}"
        return pd.read_sql(sql=query, con=self.conn, params=values)
