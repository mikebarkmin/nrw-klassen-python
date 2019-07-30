import pyodbc
from typing import Optional
from query_result import QueryResult


class DatabaseConnector():
    """
    Ein Objekt der Klasse DatabaseConnector ermoeglicht die Abfrage und Manipulation 
    einer MySQL-Datenbank. 
    Beim Erzeugen des Objekts wird eine Datenbankverbindung aufgebaut, so dass 
    anschließend SQL-Anweisungen an diese Datenbank gerichtet werden koennen.
    """

    def __init__(self, p_ip: str, p_port: int, p_database: str, p_username: str, p_password: str):
        """
        Ein Objekt vom Typ DatabaseConnector wird erstellt, und eine Verbindung zur Datenbank 
        wird aufgebaut. Mit den Parametern p_ip und p_port werden die IP-Adresse und die 
        Port-Nummer uebergeben, unter denen die Datenbank mit Namen p_database zu erreichen ist. 
        Mit den Parametern p_username und p_password werden Benutzername und Passwort fuer die 
        Datenbank uebergeben.
        """
        super().__init__()
        try:
            self._connection = pyodbc.connect(
                f'DRIVER=Devart ODBC Driver for MySQL;SERVER={p_ip};DATABASE={p_database};UID={p_username};PWD={p_password}')
        except Exception as e:
            self._message: Optional[str] = str(e)

    def execute_statement(self, p_sql_statement: str):
        """
        Der Auftrag schickt den im Parameter p_sql_statement enthaltenen SQL-Befehl an die 
        Datenbank ab. 
        Handelt es sich bei p_sql_statement um einen SQL-Befehl, der eine Ergebnismenge 
        liefert, so kann dieses Ergebnis anschließend mit der Methode get_current_query_result 
        abgerufen werden.
        """
        self._current_query_result = None
        self._message = None

        if self._connection is None:
            self.__message = "No connection"
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
        """
        Die Anfrage liefert das Ergebnis des letzten mit der Methode executeStatement an 
        die Datenbank geschickten SQL-Befehls als Ob-jekt vom Typ QueryResult zurueck.
        Wurde bisher kein SQL-Befehl abgeschickt oder ergab der letzte Aufruf von 
        executeStatement keine Ergebnismenge (z.B. bei einem INSERT-Befehl oder einem 
        Syntaxfehler), so wird None geliefert.  
        """
        return self._current_query_result

    def get_error_message(self) -> Optional[str]:
        """
        Die Anfrage liefert None oder eine Fehlermeldung, die sich jeweils auf die letzte zuvor ausgefuehrte 
        Datenbankoperation bezieht.
        """
        return self._message

    def close(self):
        """
        Die Datenbankverbindung wird geschlossen.
        """
        try:
            self._connection.close()
        except Exception as e:
            self._message = str(e)
