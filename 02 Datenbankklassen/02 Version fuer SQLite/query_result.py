from typing import List


class QueryResult():
    """
    Ein Objekt der Klasse QueryResult stellt die Ergebnistabelle einer Datenbankanfrage mit Hilfe 
    der Klasse DatabaseConnector dar. Objekte dieser Klasse werden nur von der Klasse DatabaseConnector erstellt. 
    Die Klasse verfuegt ueber keinen oeffentlichen Konstruktor.
    """

    def __init__(self, p_data: List[List[str]], p_column_names: List[str], p_column_types: List[str]):
        self.__data = p_data
        self.__column_names = p_column_names
        self.__column_types = p_column_types

    def get_data(self) -> List[List[str]]:
        """
        Die Anfrage liefert die Eintraege der Ergebnistabelle als zweidimensionales Feld
        vom Typ String. Der erste Index des Feldes stellt die Zeile und der zweite die 
        Spalte dar (d.h. Object[zeile][spalte]).
        """
        return self.__data

    def get_column_names(self) -> List[str]:
        """
        Die Anfrage liefert die Bezeichner der Spalten der Ergebnistabelle als Feld vom 
        Typ String zurueck.
        """
        return self.__column_names

    def get_column_types(self) -> List[str]:
        """
        Die Anfrage liefert die Typenbezeichnung der Spalten der Ergebnistabelle als Feld 
        vom Typ String zurueck. Die Bezeichnungen entsprechen den Angaben in der Datenbank.
        """
        return self.__column_types

    def get_row_count(self) -> int:
        """
        Die Anfrage liefert die Anzahl der Zeilen der Ergebnistabelle als Integer.
        """
        if self.__data is not None:
            return len(self.__data)
        else:
            return 0

    def get_column_count(self) -> int:
        """
        Die Anfrage liefert die Anzahl der Spalten der Ergebnistabelle als Integer.
        """
        if self.__data is not None and len(self.__data) > 0 and self.__data[0] is not None:
            return len(self.__data[0])
        else:
            return 0

