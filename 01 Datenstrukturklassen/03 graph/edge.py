from typing import List
from vertex import Vertex


class Edge():
    """
    Die Klasse Edge stellt eine einzelne, ungerichtete Kante eines Graphen dar. 
    Beim Erstellen werden die beiden durch sie zu verbindenden Knotenobjekte und eine 
    Gewichtung als float uebergeben. Beide Knotenobjekte koennen abgefragt werden. 
    Des Weiteren koennen die Gewichtung und eine Markierung gesetzt und abgefragt werden.
    """

    def __init__(self, p_vertex: Vertex, p_another_vertex: Vertex, p_weight: float):
        """
        Ein neues Objekt vom Typ Edge wird erstellt. Die von diesem Objekt 
        repraesentierte Kante verbindet die Knoten p_vertex und pAnotherVertex mit der 
        Gewichtung p_weight. Ihre Markierung hat den Wert False.
        """
        self.__vertices: List[Vertex] = []
        self.__vertices.append(p_vertex)
        self.__vertices.append(p_another_vertex)
        self.__weight = p_weight
        self.__mark = False

    def get_vertices(self):
        """
        Die Anfrage gibt die beiden Knoten, die durch die Kante verbunden werden, als neues Feld vom Typ Vertex zurueck. Das Feld hat 
        genau zwei Eintraege mit den Indexwerten 0 und 1.
        """
        return self.__vertices.copy()

    def get_weight(self) -> float:
        """
        Die Anfrage liefert das Gewicht der Kante als float.
        """
        return self.__weight

    def set_weight(self, p_weight: float):
        """
        Der Auftrag setzt das Gewicht der Kante auf p_weight.
        """
        self.__weight = p_weight

    def is_marked(self) -> bool:
        """
        Die Anfrage liefert True, wenn die Markierung der Kante den Wert True hat, ansonsten False.
        """
        return self.__mark

    def set_mark(self, p_mark: bool):
        """
        Der Auftrag setzt die Markierung der Kante auf den Wert p_mark.
        """
        self.__mark = p_mark
