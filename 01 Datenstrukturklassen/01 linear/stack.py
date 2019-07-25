from typing import TypeVar, Generic, Optional

ContentType = TypeVar('ContentType')
T = TypeVar('T')


class Stack(Generic[ContentType]):
    """
    Objekte der generischen Klasse Stack (Keller, Stapel) verwalten beliebige
    Objekte vom Typ ContentType nach dem Last-In-First-Out-Prinzip, d.h., das
    zuletzt abgelegte Objekt wird als erstes wieder entnommen. Alle Methoden
    haben eine konstante Laufzeit, unabhaengig von der Anzahl der verwalteten
    Objekte.
    """

    class StackNode(Generic[T]):

        def __init__(self, p_content: T):
            """
            Ein neues Objekt vom Typ StackNode wird erschaffen.
            Der Inhalt wird per Parameter gesetzt. Der Verweis ist leer.

            :param p_content: der Inhalt des Knotens
            """
            self.__content: T = p_content
            self.__next_node: Optional['Stack.StackNode'] = None

        @property
        def next(self) -> 'Optional[Stack.StackNode]':
            """
            :returns: das Objekt, auf das der aktuelle Verweis zeigt
            :rtype: Stack.StackNode
            """
            return self.__next_node

        @next.setter
        def next(self, p_next: 'Stack.StackNode'):
            """
            Der Verweis wird auf das Objekt, das als Parameter übergeben wird, gesetzt.

            :param p_next: der Nachfolger des Knotens
            """
            self.__next_node = p_next

        @property
        def content(self) -> T:
            """
            :returns: das Inhaltsobjekt vom Typ ContentType
            :rtype: ContentType
            """
            return self.__content

    def __init__(self):
        """
        Ein leerer Stapel wird erzeugt. Objekte, die in diesem Stapel verwaltet
        werden, müssen vom Typ ContentType sein.
        """
        self.__head = None

    def is_empty(self) -> bool:
        """
        Die Anfrage liefert den Wert True, wenn der Stapel keine Objekte
        enthält, sonst liefert sie den Wert False.

        :returns: True, falls der Stapel leer ist, sonst False
        :rtype: bool
        """
        return self.__head is None

    def push(self, p_content: ContentType):
        """
        Das Objekt p_content wird oben auf den Stapel gelegt. Falls
        p_content gleich null ist, bleibt der Stapel unverändert.

        :param: p_content das einzufügende Objekt vom Typ ContentType
        """
        if (p_content is not None):
            node = Stack.StackNode(p_content)
            node.next = self.__head
            self.__head = node

    def pop(self):
        """
        Das zuletzt eingefügte Objekt wird von dem Stapel entfernt. Falls der
        Stapel leer ist, bleibt er unverändert.
        """
        if not self.is_empty():
            self.__head = self.__head.next

    def top(self) -> Optional[ContentType]:
        """
        Die Anfrage liefert das oberste Stapelobjekt. Der Stapel bleibt
        unverändert. Falls der Stapel leer ist, wird null zurückgegeben.

        :returns: das oberste Stackelement vom Typ ContentType oder None, falls der Stack leer ist
        :rtype: ContentType
        """
        if not self.is_empty():
            return self.__head.content
        return None
