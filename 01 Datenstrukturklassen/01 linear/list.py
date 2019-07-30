from typing import TypeVar, Generic, Optional

ContentType = TypeVar('ContentType')


class List(Generic[ContentType]):
    """
    Objekt der generischen Klasse List verwalten beliebig viele linear
    angeordnete Objekte vom Typ ContentType. Auf hoechstens ein Listenobjekt,
    aktuellesObjekt genannt, kann jeweils zugegriffen werden.

    Wenn eine Liste leer ist, vollstaendig durchlaufen wurde oder das aktuelle
    Objekt am Ende der Liste geloescht wurde, gibt es kein aktuelles Objekt.

    Das erste oder das letzte Objekt einer Liste koennen durch einen Auftrag zum
    aktuellen Objekt gemacht werden. Ausserdem kann das dem aktuellen Objekt
    folgende Listenobjekt zum neuen aktuellen Objekt werden.

    Das aktuelle Objekt kann gelesen, veraendert oder geloescht werden. Ausserdem
    kann vor dem aktuellen Objekt ein Listenobjekt eingefuegt werden.
    """

    class ListNode():

        def __init__(self, p_content):
            """
            Ein neues Objekt wird erschaffen. Der Verweis ist leer.

            :param p_content: das Inhaltsobjekt vom Typ ContentType
            """
            self.__content = p_content
            self.__next = None

        def get_content(self):
            """
            Der Inhalt des Knotens wird zurueckgeliefert.

            :returns: das Inhaltsobjekt des Knotens
            :rtype: ContentType
            """
            return self.__content

        def set_content(self, p_content):
            """
            Der Inhalt dieses Kontens wird gesetzt.

            :param p_content: das Inhaltsobjekt vom Typ ContentType
            """
            self.__content = p_content

        def get_next_node(self) -> 'List.ListNode':
            """
            Der Nachfolgeknoten wird zurueckgeliefert.

            :returns: das Objekt, auf das der aktuelle Verweis zeigt
            :rtype: List.ListNode
            """
            return self.__next

        def set_next_node(self, p_next: 'List.ListNode'):
            """
            Der Verweis wird auf das Objekt, das als Parameter uebergeben
            wird, gesetzt.

            :param p_next: der Nachfolger des Knotens
            """
            self.__next = p_next

    def __init__(self):
        """
        Eine leere Liste wird erzeugt.
        """
        self._first = None
        self._last = None
        self._current = None

    def is_empty(self):
        """
        Die Anfrage liefert den Wert True, wenn die Liste keine Objekte enthaelt,
        sonst liefert sie den Wert False.

        :returns: True, wenn die Liste leer ist, sonst False
        :rtype: bool
        """
        return self._first is None

    def has_access(self):
        """
        Die Anfrage liefert den Wert True, wenn es ein aktuelles Objekt gibt,
        sonst liefert sie den Wert False.

        :returns: True, falls Zugriff moeglich, sonst False
        :rtype: bool
        """
        return self._current is not None

    def next(self):
        """
        Falls die Liste nicht leer ist, es ein aktuelles Objekt gibt und dieses
        nicht das letzte Objekt der Liste ist, wird das dem aktuellen Objekt in
        der Liste folgende Objekt zum aktuellen Objekt, andernfalls gibt es nach
        Ausfuehrung des Auftrags kein aktuelles Objekt, d.h. has_access() liefert
        den Wert False.
        """
        if self.has_access():
            self._current = self._current.get_next_node()

    def to_first(self):
        """
        Falls die Liste nicht leer ist, wird das erste Objekt der Liste aktuelles
        Objekt. Ist die Liste leer, geschieht nichts.
        """
        if not self.is_empty():
            self._current = self._first

    def to_last(self):
        """
        Falls die Liste nicht leer ist, wird das letzte Objekt der Liste
        aktuelles Objekt. Ist die Liste leer, geschieht nichts.
        """
        if not self.is_empty():
            self._current = self._last

    def get_content(self) -> Optional[ContentType]:
        """
        Falls es ein aktuelles Objekt gibt (has_access() == True), wird das
        aktuelle Objekt zurueckgegeben, andernfalls (has_access() == False) gibt
        die Anfrage den Wert None zurueck.

        :returns: das aktuelle Objekt (vom Typ ContentType) oder None, wenn es
                kein aktuelles Objekt gibt
        :rtype: ContentType
        """
        if self.has_access():
            return self._current.get_content()
        else:
            return None

    def set_content(self, p_content: ContentType):
        """
        Falls es ein aktuelles Objekt gibt (has_access() == True) und p_content
        ungleich None ist, wird das aktuelle Objekt durch p_content ersetzt. Sonst
        geschieht nichts.

        :param p_content:
                    das zu schreibende Objekt vom Typ ContentType
        """
        if p_content is not None and self.has_access():
            self._current.set_content(p_content)

    def insert(self, p_content: ContentType):
        """
        Falls es ein aktuelles Objekt gibt (has_access() == True), wird ein neues
        Objekt vor dem aktuellen Objekt in die Liste eingefuegt. Das aktuelle
        Objekt bleibt unveraendert.

        Wenn die Liste leer ist, wird p_content in die Liste eingefuegt und es
        gibt weiterhin kein aktuelles Objekt (has_access() == False).

        Falls es kein aktuelles Objekt gibt (has_access() == False) und die Liste
        nicht leer ist oder p_content gleich None ist, geschieht nichts.

        :param p_content:
                    das einzufuegende Objekt vom Typ ContentType
        """
        if p_content is not None:
            if self.has_access():
                new_node = List.ListNode(p_content)

                if self._current is not self._first:
                    previous = self.get_previous(self._current)
                    if previous is not None:
                        new_node.set_next_node(previous.get_next_node())
                        previous.set_next_node(new_node)
                else:
                    new_node.set_next_node(self._first)
                    self._first = new_node
            else:
                if self.is_empty():
                    new_node = List.ListNode(p_content)

                    self._first = new_node
                    self._last = new_node

    def append(self, p_content: ContentType):
        """
        Falls p_content gleich None ist, geschieht nichts.

        Ansonsten wird ein neues Objekt p_content am Ende der Liste eingefuegt.
        Das aktuelle Objekt bleibt unveraendert.

        Wenn die Liste leer ist, wird das Objekt p_content in die Liste eingefuegt
        und es gibt weiterhin kein aktuelles Objekt (has_access() == False).

        :param p_content:
                    das anzuhaengende Objekt vom Typ ContentType
        """
        if p_content is not None:
            if self.is_empty():
                self.insert(p_content)
            else:
                new_node = List.ListNode(p_content)

                self._last.set_next_node(new_node)
                self._last = new_node

    def concat(self, p_list: 'List[ContentType]'):
        """
        Falls es sich bei der Liste und p_list um dasselbe Objekt handelt,
        p_list None oder eine leere Liste ist, geschieht nichts.

        Ansonsten wird die Liste p_list an die aktuelle Liste angehaengt.
        Anschliessend wird p_list eine leere Liste. Das aktuelle Objekt bleibt
        unveraendert. Insbesondere bleibt has_access identisch.

        :param p_list:
                    die am Ende anzuhaengende Liste vom Typ List<ContentType>
        """
        if p_list is not self and p_list is not None and not p_list.is_empty():
            if self.is_empty():
                self._first = p_list._first
                self._last = p_list._last
            else:
                self._last.set_next_node(p_list._first)
                self._last = p_list._last

            p_list._first = None
            p_list._last = None
            p_list._current = None

    def remove(self):
        """
        Wenn die Liste leer ist oder es kein aktuelles Objekt gibt (has_access()
        == False), geschieht nichts.

        Falls es ein aktuelles Objekt gibt (has_access() == True), wird das
        aktuelle Objekt geloescht und das Objekt hinter dem geloeschten Objekt
        wird zum aktuellen Objekt.

        Wird das Objekt, das am Ende der Liste steht, geloescht, gibt es kein
        aktuelles Objekt mehr.
        """
        if self.has_access() and not self.is_empty():
            if self._current is self._first:
                self._first = self._first.get_next_node()
            else:
                previous = self.get_previous(self._current)
                if self._current is self._last:
                    self._last = previous
                previous.set_next_node(self._current.get_next_node())

            temp = self._current.get_next_node()
            self._current.set_content(None)
            self._current.set_next_node(None)
            self._current = temp

            if self.is_empty():
                self._last = None

    def get_previous(self, p_node: 'List.ListNode') -> Optional['List.ListNode']:
        """
        Liefert den Vorgaengerknoten des Knotens pNode. Ist die Liste leer, p_node
        == None, p_node nicht in der Liste oder p_node der erste Knoten der Liste,
        wird None zurueckgegeben.

        :param p_node:
                der Knoten, dessen Vorgaenger zurueckgegeben werden soll
        :returns: der Vorgaenger des Knotens p_node oder None, falls die Liste leer ist,
                p_node == None ist, p_node nicht in der Liste ist oder p_Node der erste Knoten
                der Liste ist
        """
        if p_node is not None and p_node is not self._first and not self.is_empty():
            temp = self._first
            while temp is not None and temp.next is not p_node:
                temp = temp.get_next_node()
            return temp
        else:
            return None
