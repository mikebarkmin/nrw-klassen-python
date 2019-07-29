from typing import Optional
from list import List
from vertex import Vertex
from edge import Edge


class Graph():
    """
    Die Klasse Graph stellt einen ungerichteten, kantengewichteten Graphen dar. Es koennen 
    Knoten- und Kantenobjekte hinzugefuegt und entfernt, flache Kopien der Knoten- und Kantenlisten 
    des Graphen angefragt und Markierungen von Knoten und Kanten gesetzt und ueberprueft werden.
    Des Weiteren kann eine Liste der Nachbarn eines bestimmten Knoten, eine Liste der inzidenten 
    Kanten eines bestimmten Knoten und die Kante von einem bestimmten Knoten zu einem 
    anderen bestimmten Knoten angefragt werden. Abgesehen davon kann abgefragt werden, welches 
    Knotenobjekt zu einer bestimmten ID gehoert und ob der Graph leer ist.
    """

    def __init__(self):
        """
        Ein Objekt vom Typ Graph wird erstellt. Der von diesem Objekt 
        repraesentierte Graph ist leer.
        """
        self.__vertices = List[Vertex]()
        self.__edges = List[Edge]()

    def get_vertices(self) -> List[Vertex]:
        """
        Die Anfrage liefert eine neue Liste aller Knotenobjekte vom Typ List<Vertex>.
        """
        result = List[Vertex]()
        self.__vertices.to_first()
        while self.__vertices.has_access():
            result.append(self.__vertices.get_content())
            self.__vertices.next()

        result.to_first()
        return result

    def get_edges(self, p_vertex: Vertex = None) -> List[Edge]:
        """
        Die Anfrage liefert eine neue Liste alle inzidenten Kanten zum Knoten p_vertex oder alle Kanten,
        wenn p_vertex None ist. Hat der Knoten p_vertex keine inzidenten Kanten in diesem Graphen oder
        ist gar nicht in diesem Graphen enthalten, so wird eine leere Liste zurueckgeliefert.
        """
        result = List[Edge]()

        self.__edges.to_first()
        while self.__edges.has_access():
            vertex_pair = self.__edges.get_content().get_vertices()

            if p_vertex is None:
                result.append(self.__edges.get_content())
            elif vertex_pair[0] == p_vertex:
                result.append(self.__edges.get_content())
            elif vertex_pair[1] == p_vertex:
                result.append(self.__edges.get_content())

            self.__edges.next()

        return result

    def get_vertex(self, p_id: str) -> Optional[Vertex]:
        """
        Die Anfrage liefert das Knotenobjekt mit p_iD als ID. Ist ein solchen Knotenobjekt nicht im Graphen enthalten,
        wird None zurueckgeliefert.
        """
        result = None
        self.__vertices.to_first()
        while self.__vertices.has_access() and result is None:
            if self.__vertices.get_content().get_id() == p_id:
                result = self.__vertices.get_content()
            self.__vertices.next()

        return result

    def add_vertex(self, p_vertex: Vertex):
        """
        Der Auftrag fuegt den Knoten p_vertex in den Graphen ein, sofern es noch keinen
        Knoten mit demselben ID-Eintrag wie p_vertex im Graphen gibt und p_vertex eine ID ungleich None hat. 
        Ansonsten passiert nichts.
        """
        if p_vertex is not None and p_vertex.get_id() is not None:
            free_id = True
            self.__vertices.to_first()
            while self.__vertices.has_access() and free_id:
                if self.__vertices.get_content().get_id() == p_vertex.get_id():
                    free_id = False
                self.__vertices.next()

            if free_id:
                self.__vertices.append(p_vertex)

    def add_edge(self, p_edge: Edge):
        """
        Der Auftrag fuegt die Kante p_edge in den Graphen ein, sofern beide durch die Kante verbundenen Knoten
        im Graphen enthalten sind, nicht identisch sind und noch keine Kante zwischen den Knoten existiert. Ansonsten passiert nichts.
        """
        if p_edge is not None:
            vertex_pair = p_edge.get_vertices()

            if vertex_pair[0] is not None and vertex_pair[1] is not None and \
                    self.get_vertex(vertex_pair[0].get_id()) == vertex_pair[0] and \
                    self.get_vertex(vertex_pair[1].get_id()) == vertex_pair[1] and \
                    self.get_edge(vertex_pair[0], vertex_pair[1]) is None and \
                    vertex_pair[0] is not vertex_pair[1]:
                self.__edges.append(p_edge)

    def remove_vertex(self, p_vertex: Vertex):
        """
        Der Auftrag entfernt den Knoten p_vertex aus dem Graphen und loescht alle Kanten, die mit ihm inzident sind.
        Ist der Knoten p_vertex nicht im Graphen enthalten, passiert nichts.
        """
        self.__edges.to_first()
        while self.__edges.has_access():
            akt = self.__edges.get_content().get_vertices()
            if akt[0] == p_vertex or akt[1] == p_vertex:
                self.__edges.remove()
            else:
                self.__edges.next()

        self.__vertices.to_first()
        while self.__vertices.has_access() and self.__vertices.get_content() is not p_vertex:
            self.__vertices.next()

        if self.__vertices.has_access():
            self.__vertices.remove()

    def remove_edge(self, p_edge: Edge):
        """
        Der Auftrag entfernt die Kante p_edge aus dem Graphen. Ist die Kante p_edge nicht 
        im Graphen enthalten, passiert nichts.
        """
        self.__edges.to_first()
        while self.__edges.has_access():
            if self.__edges.get_content() == p_edge:
                self.__edges.remove()
            else:
                self.__edges.next()

    def set_all_vertex_marks(self, p_mark: bool):
        """
        Der Auftrag setzt die Markierungen aller Knoten des Graphen auf p_mark.
        """
        self.__vertices.to_first()

        while self.__vertices.has_access():
            self.__vertices.get_content().set_mark(p_mark)
            self.__vertices.next()

    def set_all_edge_marks(self, p_mark: bool):
        """
        Der Auftrag setzt die Markierungen aller Kanten des Graphen auf p_mark.
        """
        self.__edges.to_first()

        while self.__edges.has_access():
            self.__edges.get_content().set_mark(p_mark)
            self.__edges.next()

    def all_vertices_marked(self) -> bool:
        """
        Die Anfrage liefert True, wenn alle Knoten des Graphen mit True markiert sind, ansonsten False.
        """
        result = True
        self.__vertices.to_first()
        while self.__vertices.has_access():
            if not self.__vertices.get_content().is_marked():
                result = False
            self.__vertices.next()
        return result

    def all_edges_marked(self) -> bool:
        """
        Die Anfrage liefert True, wenn alle Kanten des Graphen mit True markiert sind, ansonsten False.
        """
        result = True
        self.__edges.to_first()
        while self.__edges.has_access():
            if not self.__edges.get_content().is_marked():
                result = False
            self.__edges.next()
        return result

    def get_neighbours(self, p_vertex: Vertex) -> List[Vertex]:
        """
        Die Anfrage liefert alle Nachbarn des Knotens p_vertex als neue Liste vom Typ List<Vertex>. Hat der Knoten
        p_vertex keine Nachbarn in diesem Graphen oder ist gar nicht in diesem Graphen enthalten, so 
        wird eine leere Liste zurueckgeliefert.
        """
        result = List[Vertex]()

        self.__edges.to_first()
        while self.__edges.has_access():
            vertex_pair = self.__edges.get_content().get_vertices()

            if vertex_pair[0] == p_vertex:
                result.append(vertex_pair[1])
            elif vertex_pair[1] == p_vertex:
                result.append(vertex_pair[0])

            self.__edges.next()

        return result

    def get_edge(self, p_vertex: Vertex, p_another_vertex: Vertex) -> Optional[Edge]:
        """
        Die Anfrage liefert die Kante, welche die Knoten p_vertex und p_another_vertex verbindet, 
        als Objekt vom Typ Edge. Ist der Knoten p_vertex oder der Knoten p_another_vertex nicht 
        im Graphen enthalten oder gibt es keine Kante, die beide Knoten verbindet, so wird None 
        zurueckgeliefert.
        """
        result = None

        self.__edges.to_first()
        while self.__edges.has_access() and result is None:
            vertex_pair = self.__edges.get_content().get_vertices()
            if (vertex_pair[0] == p_vertex and vertex_pair[1] == p_another_vertex) or \
                    (vertex_pair[0] == p_another_vertex and vertex_pair[1] == p_vertex):
                result = self.__edges.get_content()

            self.__edges.next()

        return result

    def is_empty(self) -> bool:
        """
        Die Anfrage liefert True, wenn der Graph keine Knoten enthaelt, ansonsten False.
        """
        return self.__vertices.is_empty()
