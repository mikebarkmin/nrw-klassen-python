import unittest

from graph import Graph
from vertex import Vertex
from edge import Edge


class TestGraph(unittest.TestCase):
    def test_add_vertex(self):
        g = Graph()
        v = Vertex(0)
        g.add_vertex(v)

        self.assertFalse(g.is_empty())
        self.assertEqual(g.get_vertex(0), v)

    def test_add_edge(self):
        g = Graph()

        v1 = Vertex(0)
        v2 = Vertex(1)

        g.add_vertex(v1)
        self.assertEqual(g.get_vertex(0), v1)
        self.assertNotEqual(g.get_vertex(1), v2)

        e = Edge(v1, v2, 3)
        g.add_edge(e)
        self.assertTrue(g.get_edges().is_empty())

        g.add_vertex(v2)
        g.add_edge(e)
        self.assertFalse(g.get_edges().is_empty())

    def test_remove_vertex(self):
        g = Graph()

        v1 = Vertex(0)
        v2 = Vertex(1)
        v3 = Vertex(2)

        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_vertex(v3)

        self.assertFalse(g.is_empty())

        vertices = g.get_vertices()
        num_vertices = 0
        vertices.to_first()
        while vertices.has_access():
            num_vertices += 1
            vertices.next()
        self.assertEqual(num_vertices, 3)

        g.remove_vertex(v1)
        vertices = g.get_vertices()
        num_vertices = 0
        vertices.to_first()
        while vertices.has_access():
            num_vertices += 1
            vertices.next()
        self.assertEqual(num_vertices, 2)


if __name__ == '__main__':
    unittest.main()
