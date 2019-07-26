from typing import Generic, TypeVar, Optional
from comparable_content import ComparableContent

ContentType = TypeVar("ContentType")


class BinarySearchTree(Generic[ContentType]):
    """
    Mithilfe der generischen Klasse BinarySearchTree koennen beliebig viele
    Objekte in einem Binaerbaum (binaerer Suchbaum) entsprechend einer
    Ordnungsrelation verwaltet werden.

    Ein Objekt der Klasse stellt entweder einen leeren binaeren Suchbaum dar oder
    verwaltet ein Inhaltsobjekt sowie einen linken und einen rechten Teilbaum,
    die ebenfalls Objekte der Klasse BinarySearchTree sind.

    Die Klasse der Objekte, die in dem Suchbaum verwaltet werden sollen, muss
    das generische Interface ComparableContent implementieren. Dabei muss durch
    Ueberschreiben der drei Vergleichsmethoden isLess, isEqual, isGreater (s.
    Dokumentation des Interfaces) eine eindeutige Ordnungsrelation festgelegt
    sein.

    Alle Objekte im linken Teilbaum sind kleiner als das Inhaltsobjekt des
    binaeren Suchbaums. Alle Objekte im rechten Teilbaum sind groesser als das
    Inhaltsobjekt des binaeren Suchbaums. Diese Bedingung gilt (rekursiv) auch in
    beiden Teilbaeumen.

    Hinweis: In dieser Version wird die Klasse BinaryTree nicht benutzt.
    """

    class BSTNode():
        """
        Durch diese innere Klasse kann man dafuer sorgen, dass ein leerer Baum
        null ist, ein nicht-leerer Baum jedoch immer eine nicht-None-Wurzel sowie
        nicht-None-Teilbaeume hat.
        """

        def __init__(self, p_content: ComparableContent):
            """
            Der Knoten hat einen linken und rechten Teilbaum, die 
            beide von None verschieden sind. Also hat ein Blatt immer zwei 
            leere Teilbaeume unter sich.
            """
            self._content: ComparableContent = p_content
            self._left: 'BinarySearchTree' = BinarySearchTree()
            self._right: 'BinarySearchTree' = BinarySearchTree()

    def __init__(self):
        """
        Der Konstruktor erzeugt einen leeren Suchbaum.
        """
        self.__node = None

    def is_empty(self) -> bool:
        """
        Diese Anfrage liefert den Wahrheitswert True, wenn der Suchbaum leer ist,
        sonst liefert sie den Wert False.

        :returns: True, wenn der binaere Suchbaum leer ist, sonst False
        """
        return self.__node is None

    def insert(self, p_content: ComparableContent[ContentType]):
        """
        Falls der Parameter null ist, geschieht nichts.

        Falls ein bezueglich der verwendeten Vergleichsmethode is_equal mit
        p_content uebereinstimmendes Objekt im geordneten binaeren Suchbau
        enthalten ist, passiert nichts.

        Achtung: hier wird davon ausgegangen, dass is_equal genau dann true
        liefert, wenn isLess und is_greater false liefern.

        Andernfalls (is_less oder is_greater) wird das Objekt p_content entsprechend
        der vorgegebenen Ordnungsrelation in den BinarySearchTree eingeordnet.

        :param p_content:
                   einzufuegendes Objekt vom Typ ContentType
        """
        if p_content is not None:
            if self.is_empty():
                self.__node = BinarySearchTree.BSTNode(p_content)
            elif p_content.is_less(self.__node._content):
                self.__node._left.insert(p_content)
            elif p_content.is_greater(self.__node._content):
                self.__node._right.insert(p_content)

    def get_content(self) -> Optional[ContentType]:
        """
        Diese Anfrage liefert das Inhaltsobjekt des Suchbaumes. Wenn der Suchbaum
        leer ist, wird None zurueckgegeben.

        :returns: das Inhaltsobjekt vom Typ ContentType bzw. None, wenn der aktuelle
                Suchbaum leer ist
        """
        if self.is_empty() or self.__node is None:
            return None
        else:
            return self.__node._content

    def get_left_tree(self) -> Optional['BinarySearchTree']:
        """
        Diese Anfrage liefert den linken Teilbaum des binaeren Suchbaumes.
        Wenn er leer ist, wird None zurueckgegeben.

        :returns: den linken Teilbaum (Objekt vom Typ BinarySearchTree<ContentType>) 
                bzw. None, wenn der Suchbaum leer ist
        """
        if self.is_empty():
            return None
        else:
            return self.__node._left

    def get_right_tree(self) -> Optional['BinarySearchTree']:
        """
        Diese Anfrage liefert den rechten Teilbaum des binaeren Suchbaumes.
        Wenn er leer ist, wird None zurueckgegeben.

        :returns: den rechten Teilbaum (Objekt vom Typ BinarySearchTree<ContentType>) 
                bzw. None, wenn der Suchbaum leer ist
        """
        if self.is_empty():
            return None
        else:
            return self.__node._right

    def remove(self, p_content: ComparableContent[ContentType]):
        """
        Falls ein bezueglich der verwendeten Vergleichsmethode mit
        p_content uebereinstimmendes Objekt im binaeren Suchbaum enthalten
        ist, wird dieses entfernt. Falls der Parameter None ist, aendert sich
        nichts.

        :param p_content:
                   zu entfernendes Objekt vom Typ ContentType
        """
        if self.is_empty() or p_content is None:
            return

        if p_content.is_less(self.__node._content):
            self.__node._left.remove(p_content)
        elif p_content.is_greater(self.__node._content):
            self.__node._right.remove(p_content)
        else:
            if self.__node._left.is_empty():
                if self.__node._right.is_empty():
                    self.__node = None
                else:
                    self.__node = self.__get_node_of_right_successor()
            elif self.__node._right.is_empty():
                self.__node = self.__get_node_of_left_successor()
            else:
                if self.__get_node_of_right_successor()._left.is_empty():
                    self.__node._content = self.__get_node_of_right_successor()._content
                    self.__node._right = self.__get_node_of_right_successor()._right
                else:
                    previous = self.__node._right.__ancestor_of_small_right()
                    smallest = previous.__node._left
                    self.__node._content = smallest.__node._content
                    previous.remove(smallest.__node._content)

    def search(self, p_content: ComparableContent[ContentType]) -> Optional[ContentType]:
        """
        Falls ein bezueglich der verwendeten Vergleichsmethode is_equal mit
        p_content uebereinstimmendes Objekt im binaeren Suchbaum enthalten ist,
        liefert die Anfrage dieses, ansonsten wird None zurueckgegeben.

        Falls der Parameter None ist, wird None zurueckgegeben.

        :param p_content:
                   zu suchendes Objekt vom Typ ContentType
        :returns: das gefundene Objekt vom Typ ContentType, bei erfolgloser Suche None
        """
        if self.is_empty() or p_content is None:
            return None

        content = self.get_content()
        if content is None:
            return None

        if p_content.is_less(content):
            tree = self.get_left_tree()
            if tree:
                return tree.search(p_content)
            else:
                return None
        elif p_content.is_greater(content):
            tree = self.get_right_tree()
            if tree:
                return tree.search(p_content)
            else:
                return None
        elif p_content.is_equal(content):
            return content
        else:
            return None

    def __ancestor_of_small_right(self):
        """
        Die Methode liefert denjenigen Baum, dessen linker Nachfolger keinen linken
        Nachfolger mehr hat. Es ist also spaeter moeglich, in einem Baum im
        rechten Nachfolger den Vorgaenger des linkesten Nachfolgers zu finden.
        """
        if self.__get_node_of_left_successor()._left.is_empty():
            return self
        else:
            return self.__node._left.__ancestor_of_small_right

    def __get_node_of_left_successor(self):
        return self.__node._left.__node

    def __get_node_of_right_successor(self):
        return self.__node._right.__node

