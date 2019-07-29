class Vertex():
    """
    Die Klasse Vertex stellt einen einzelnen Knoten eines Graphen dar. Jedes Objekt 
    dieser Klasse verfuegt ueber eine im Graphen eindeutige ID als String und kann diese 
    ID zurueckliefern. Darueber hinaus kann eine Markierung gesetzt und abgefragt werden.
    """

    def __init__(self, p_id: str):
        """
        Ein neues Objekt vom Typ Vertex wird erstellt. Seine Markierung hat den Wert False.
        """
        self.__id = p_id
        self.__mark = False

    def get_id(self) -> str:
        """
        Die Anfrage liefert die ID des Knotens als String.
        """
        return self.__id

    def is_marked(self) -> bool:
        """
        Der Auftrag setzt die Markierung des Knotens auf den Wert p_mark.
        """
        return self.__mark

    def set_mark(self, p_mark: bool):
        """
        Die Anfrage liefert True, wenn die Markierung des Knotens den Wert True hat, ansonsten False.
        """
        self.__mark = p_mark
