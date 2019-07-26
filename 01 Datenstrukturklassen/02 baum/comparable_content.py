from typing import Generic, TypeVar
import abc

ContentType = TypeVar("ContentType")


class ComparableContent(Generic[ContentType], abc.ABC):
    """
    Das generische Interface ComparableContent<ContentType> legt die Methoden
    fest, ueber die Objekte verfuegen muessen, die in einen binaeren Suchbaum
    (BinarySearchTree) eingefuegt werden sollen. Die Ordnungsrelation wird in
    Klassen, die ComparableContent implementieren durch Ueberschreiben der drei
    implizit abstrakten Methoden is_greater, is_equal und is_less festgelegt.
    """
    @abc.abstractmethod
    def is_greater(self, p_content: ContentType) -> bool:
        """
        Wenn festgestellt wird, dass das Objekt, von dem die Methode aufgerufen
        wird, bzgl. der gewuenschten Ordnungsrelation groesser als das Objekt
        pContent ist, wird true geliefert. Sonst wird false geliefert.

        :param p_content:
                    das mit dem aufrufenden Objekt zu vergleichende Objekt vom
                    Typ ContentType
        :returns: True, wenn das aufrufende Objekt groesser ist als das Objekt
                p_content, sonst False
        :rtype: bool
        """
        pass

    @abc.abstractmethod
    def is_equal(self, p_content: ContentType) -> bool:
        """
        Wenn festgestellt wird, dass das Objekt, von dem die Methode aufgerufen
        wird, bzgl. der gewuenschten Ordnungsrelation gleich gross wie das Objekt
        pContent ist, wird true geliefert. Sonst wird false geliefert.

        :param p_content:
                    das mit dem aufrufenden Objekt zu vergleichende Objekt vom
                    Typ ContentType
        :returns: True, wenn das aufrufende Objekt gleich gross ist wie das Objekt
                p_content, sonst False
        :rtype: bool
        """
        pass

    @abc.abstractmethod
    def is_less(self, p_content: ContentType) -> bool:
        """
        Wenn festgestellt wird, dass das Objekt, von dem die Methode aufgerufen
        wird, bzgl. der gewuenschten Ordnungsrelation kleiner als das Objekt
        pContent ist, wird true geliefert. Sonst wird false geliefert.

        :param p_content:
                    das mit dem aufrufenden Objekt zu vergleichende Objekt vom
                    Typ ContentType
        :returns: True, wenn das aufrufende Objekt kleiner ist als das Objekt
                p_content, sonst False
        :rtype: bool
        """
        pass
