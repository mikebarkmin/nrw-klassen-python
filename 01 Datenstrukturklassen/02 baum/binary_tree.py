from typing import Generic, TypeVar, Optional

ContentType = TypeVar("ContentType")


class BinaryTree(Generic[ContentType]):
    """
    Mithilfe der generischen Klasse BinaryTree koennen beliebig viele
    Inhaltsobjekte vom Typ ContentType in einem Binaerbaum verwaltet werden. Ein
    Objekt der Klasse stellt entweder einen leeren Baum dar oder verwaltet ein
    Inhaltsobjekt sowie einen linken und einen rechten Teilbaum, die ebenfalls
    Objekte der generischen Klasse BinaryTree sind.
    """

    class BTNode():
        """
        Durch diese innere Klasse kann man dafuer sorgen, dass ein leerer Baum
        null ist, ein nicht-leerer Baum jedoch immer eine nicht-null-Wurzel sowie
        nicht-null-Teilbaeume, ggf. leere Teilbaeume hat.
        """

        def __init__(self, p_content):
            """
            Der Knoten hat einen linken und einen rechten Teilbaum, die
            beide von null verschieden sind. Also hat ein Blatt immer zwei
            leere Teilbaeume unter sich.

            :param p_content: Inhalt des Knotens
            """
            self._content = p_content
            self._left: Optional['BinaryTree'] = BinaryTree()
            self._right: Optional['BinaryTree'] = BinaryTree()

    def __init__(self, p_content: ContentType = None,
                 left_tree: 'BinaryTree' = None,
                 right_tree: 'BinaryTree' = None):
        """
        Wenn der Parameter p_content ungleich None ist, wird ein Binaerbaum mit
        p_content als Inhalt und den beiden Teilbaeume left_tree und right_tree
        erzeugt. Sind left_tree oder right_tree gleich None, wird der
        entsprechende Teilbaum als leerer Binaerbaum eingefuegt. So kann es also
        nie passieren, dass linke oder rechte Teilbaeume null sind. Wenn der
        Parameter p_content gleich None ist, wird ein leerer Binaerbaum erzeugt.

        :param p_content:
                   das Inhaltsobjekt des Wurzelknotens vom Typ ContentType
        :param left_tree:
                   der linke Teilbaum vom Typ BinaryTree<ContentType>
        :param right_tree:
                   der rechte Teilbaum vom Typ BinaryTree<ContentType>
        """
        self.__node = None

        if p_content is not None:
            self.__node = BinaryTree.BTNode(p_content)

            if left_tree is not None:
                self.__node._left = left_tree

            if right_tree is not None:
                self.__node._right = right_tree

    def is_empty(self) -> bool:
        """
        Diese Anfrage liefert den Wahrheitswert True, wenn der Binaerbaum leer
        ist, sonst liefert sie den Wert False.

        :returns: True, wenn der Binaerbaum leer ist, sonst False
        :rtype: bool
        """
        return self.__node is None

    def set_content(self, p_content: ContentType):
        """
        Wenn p_content None ist, geschieht nichts. <br />
        Ansonsten: Wenn der Binaerbaum leer ist, wird der Parameter p_content als
        Inhaltsobjekt sowie ein leerer linker und rechter Teilbaum eingefuegt.
        Ist der Binaerbaum nicht leer, wird das Inhaltsobjekt durch p_content
        ersetzt. Die Teilbaeume werden nicht geaendert.

        :param p_content:
                   neues Inhaltsobjekt vom Typ ContentType
        """
        if p_content is not None:
            if self.is_empty():
                self.__node = BinaryTree.BTNode(p_content)
                self.__node._left = BinaryTree()
                self.__node._right = BinaryTree()
            if self.__node is not None:
                self.__node._content = p_content

    def get_content(self) -> Optional[ContentType]:
        """
        Diese Anfrage liefert das Inhaltsobjekt des Binaerbaums. Wenn der
        Binaerbaum leer ist, wird None zurueckgegeben.

        :returns: das Inhaltsobjekt der Wurzel vom Typ ContentType bzw. None, wenn
                der Binaerbaum leer ist
        """
        if self.is_empty():
            return None
        elif self.__node is not None:
            return self.__node._content
        return None

    def set_left_tree(self, p_tree: 'BinaryTree'):
        """
        Falls der Parameter None ist, geschieht nichts. Wenn der Binaerbaum leer
        ist, wird p_tree nicht angehaengt. Andernfalls erhaelt der Binaerbaum den
        uebergebenen BinaryTree als linken Teilbaum.

        :param p_tree:
                   neuer linker Teilbaum vom Typ BinaryTree<ContentType>

        """
        if not self.is_empty() and p_tree is not None and self.__node is not None:
            self.__node._left = p_tree

    def set_right_tree(self, p_tree: 'BinaryTree'):
        """
        Falls der Parameter None ist, geschieht nichts. Wenn der Binaerbaum leer
        ist, wird p_tree nicht angehaengt. Andernfalls erhaelt der Binaerbaum den
        uebergebenen BinaryTree als rechten Teilbaum.

        :param p_tree:
                   neuer linker Teilbaum vom Typ BinaryTree<ContentType>

        """
        if not self.is_empty() and p_tree is not None and self.__node is not None:
            self.__node._right = p_tree

    def get_left_tree(self) -> Optional['BinaryTree']:
        """
        Diese Anfrage liefert den linken Teilbaum des Binaerbaumes. Wenn der
        Binaerbaum leer ist, wird None zurueckgegeben.

        :returns: linker Teilbaum vom Typ BinaryTree<ContentType> oder None, wenn
        der aktuelle Binaerbaum leer ist.
        :rtype: BinaryTree
        """
        if not self.is_empty() and self.__node is not None:
            return self.__node._left
        else:
            return None

    def get_right_tree(self) -> Optional['BinaryTree']:
        """
        Diese Anfrage liefert den rechten Teilbaum des Binaerbaumes. Wenn der
        Binaerbaum leer ist, wird None zurueckgegeben.

        :returns: rechter Teilbaum vom Typ BinaryTree<ContentType> oder None, wenn
        der aktuelle Binaerbaum leer ist.
        :rtype: BinaryTree
        """
        if not self.is_empty() and self.__node is not None:
            return self.__node._right
        else:
            return None
