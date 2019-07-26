from typing import TypeVar, Generic, Optional

ContentType = TypeVar('ContentType')


class Queue(Generic[ContentType]):
    """
    Objekte der generischen Klasse Queue (Warteschlange) verwalten beliebige
    Objekte vom Typ ContentType nach dem First-In-First-Out-Prinzip, d.h., das
    zuerst abgelegte Objekt wird als erstes wieder entnommen. Alle Methoden haben
    eine konstante Laufzeit, unabhaengig von der Anzahl der verwalteten Objekte.
    """

    class QueueNode():

        def __init__(self, p_content):
            """
            Ein neues Objekt vom Typ QueueNode wird erschaffen. 
            Der Inhalt wird per Parameter gesetzt. Der Verweis ist leer.

            :param p_content: das Inhaltselement des Knotens
            """
            self.__content = p_content
            self.__next_node = None

        @property
        def next(self) -> Optional['Queue.QueueNode']:
            """
            Liefert das nächste Element des aktuellen Knotens.

            :returns: das Objekt vom Type QueueNode, auf das der akutelle Verweis zeigt
            :rtype: Queue.QueueNode
            """
            return self.__next_node

        @next.setter
        def next(self, p_next: 'Queue.QueueNode'):
            """
            Der Verweis wird auf das Objekt, das als Parameter übergeben wird,
            gesetzt

            :param p_next: der Nachfolger des Knotens
            """
            self.__next_node = p_next

        @property
        def content(self):
            """
            Liefert das Inhaltsobjekt des Knotens vom Type ContentType.

            :returns: das Inhaltsobjekt des Knotens
            :rtype: ContentType
            """
            return self.__content

    def __init__(self):
        """
        Eine leere Schlange wird erzeugt.
        Objekte, die in dieser Schlange verwaltet werden, müssen vom Type
        ContentType sein.
        """
        self.__head = None
        self.__tail = None

    def is_empty(self) -> bool:
        """
        Die Anfrage liefert den Wert True, wenn die Schlange keine Objekte enthält,
        sonst liefert sie den Wert False.

        :returns: True, falls die Schlange leer ist, sonst False
        :rtype: bool
        """
        return self.__head is None

    def enqueue(self, p_content: ContentType):
        """
        Das Objekt p_content wird an die Schlange angehängt.
        Falls p_content gleich None ist, bleibt die Schlange unverändert.

        :param p_content: das anzuhängende Objekt vom Typ ContentType
        """
        if p_content is not None:
            new_node = Queue.QueueNode(p_content)
            if self.is_empty():
                self.__head = new_node
                self.__tail = new_node
            else:
                self.__tail.next = new_node
                self.__tail = new_node

    def dequeue(self):
        """
        Das erste Objekt wird aus der Schlange entfernt.
        Falls die Schlange leer ist, wird sie nicht verändert.
        """
        if not self.is_empty():
            self.__head = self.__head.next
            if self.is_empty():
                self.__head = None
                self.__tail = None

    def front(self) -> Optional[ContentType]:
        """
        Die Anfrage liefert das erste Objekt der Schlange.
        Die Schlange bleibt unverändert.
        Falls die Schlange leer ist, wird None zurückgegeben.

        :returns: das erste Objekt der Schlange vom Type ContentType oder None
        :rtype: ContentType
        """
        if self.is_empty():
            return None
        else:
            return self.__head.content
