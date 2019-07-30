import sqlite3
from typing import Optional
from query_result import QueryResult


class DatabaseConnector():
    """
    Ein Objekt der Klasse DatabaseConnector ermoeglicht die Abfrage und Manipulation 
    einer SQLite-Datenbank. 
    Beim Erzeugen des Objekts wird eine Datenbankverbindung aufgebaut, so dass 
    anschließend SQL-Anweisungen an diese Datenbank gerichtet werden koennen.
    """

    def __init__(self, p_ip: str, p_port: int, p_database: str, p_username: str, p_password: str):
        self.__connection: Optional[pyodbc.Connection] = None
        self.__message: Optional[str] = None
        self.__current_query_result: Optional[QueryResult] = None

        try:
            self.__connection = sqlite3.connect(p_database)
        except Exception as e:
            self.__message = str(e)

    def execute_statement(self, p_sql_statement: str):
        """
        Der Auftrag schickt den im Parameter p_sql_statement enthaltenen SQL-Befehl an die 
        Datenbank ab. 
        Handelt es sich bei p_sql_statement um einen SQL-Befehl, der eine Ergebnismenge 
        liefert, so kann dieses Ergebnis anschließend mit der Methode get_current_query_result 
        abgerufen werden.
        """
        self.__current_query_result = None
        self.__message = None

        if self.__connection is None:
            self.__message = "No connection"
            return

        try:
            cursor = self.__connection.cursor()

            if cursor.execute(p_sql_statement):
                result_column_names = []
                result_colum_types = []
                result_data = cursor.fetchall()

                for column in cursor.description:
                    result_column_names.append(column[0])
                    result_colum_types.append(column[1])

                self.__current_query_result = QueryResult(
                    result_data,
                    result_column_names,
                    result_colum_types
                )

            cursor.close()

        except Exception as e:
            self.__message = str(e)

    def get_current_query_result(self):
        """
        Die Anfrage liefert das Ergebnis des letzten mit der Methode executeStatement an 
        die Datenbank geschickten SQL-Befehls als Ob-jekt vom Typ QueryResult zurueck.
        Wurde bisher kein SQL-Befehl abgeschickt oder ergab der letzte Aufruf von 
        executeStatement keine Ergebnismenge (z.B. bei einem INSERT-Befehl oder einem 
        Syntaxfehler), so wird None geliefert.  
        """
        return self.__current_query_result

    def get_error_message(self) -> Optional[str]:
        """
        Die Anfrage liefert None oder eine Fehlermeldung, die sich jeweils auf die letzte zuvor ausgefuehrte 
        Datenbankoperation bezieht.
        """
        return self.__message

    def close(self):
        """
        Die Datenbankverbindung wird geschlossen.
        """
        try:
            self.__connection.close()
        except Exception as e:
            self.__message = str(e)
