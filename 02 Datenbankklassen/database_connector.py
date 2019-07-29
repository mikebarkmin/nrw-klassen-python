import pyodbc
from abc import ABC, abstractmethod
from typing import Optional
from query_result import QueryResult


class DatabaseConnector(ABC):

    @abstractmethod
    def __init__(self):
        self._connection: Optional[pyodbc.Cursor] = None
        self._message: Optional[str] = None

    def execute_statement(self, p_sql_statement: str):
        self._current_query_result = None
        self._message = None

        if self._connection is None:
            return

        try:
            cursor = self._connection.cursor()

            if cursor.execute(p_sql_statement):
                result_column_names = []
                result_colum_types = []
                result_data = cursor.fetchall()

                for column in cursor.description:
                    result_column_names.append(column[0])
                    result_colum_types.append(column[1])

                self._current_query_result = QueryResult(
                    result_data,
                    result_column_names,
                    result_colum_types
                )

            cursor.close()

        except Exception as e:
            self._message = str(e)

    def get_current_query_result(self):
        return self._current_query_result

    def get_error_message(self) -> Optional[str]:
        return self._message

    def close(self):
        try:
            self._connection.close()
        except Exception as e:
            self._message = str(e)


class DatabaseConnectorMySQL(DatabaseConnector):

    def __init__(self, p_ip: str, p_port: int, p_database: str, p_username: str, p_password: str):
        super().__init__()
        try:
            self._connection = pyodbc.connect(
                f'DRIVER=MySQL ODBC driver;SERVER={p_ip};DATABASE={p_database};UID={p_username};PWD={p_password}')
        except Exception as e:
            self._message: Optional[str] = str(e)


class DatabaseConnectorSQLite(DatabaseConnector):

    def __init__(self, p_ip: str, p_port: int, p_database: str, p_username: str, p_password: str):
        super().__init__()
        try:
            self._connection = pyodbc.connect(
                f'DRIVER=SQLite3;DATABASE={p_database}')
        except Exception as e:
            self._message: Optional[str] = str(e)
