# Source: https://experiencestack.co/graph-implementation-in-python-916fc3b6a8a

class Vertex:
    def __init__(self, vertex_id, coordinates):
        self.id = vertex_id
        self.neighbours = []
        self.coordinates = coordinates
        self.heat_level = 0


    def add_neighbour(self, vertex):
        if vertex not in self.neighbours:
            self.neighbours.append(vertex)

    def is_neighbour(self, vertex):
        if vertex in self.neighbours:
            return True
        return False

    def increase_heat(self):
        self.heat_level += 1

class Edge:
    def __init__(self, v1, v2):
        self.vertex1 = v1
        self.vertex2 = v2
        self.vertices = [v1, v2]
        self.route_num = 0
        self.routes = {}

    # def add_route(self, route):
    #     self.routes.append(route)
    #     self.route_num += 1

class Route:
    def __init__(self, endpoint1, endpoint2):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2
        self.current_node = endpoint1
        self.path = []

    def traverse_edge(self, edge):
        if current_node.is_neighbour(edge.vertex1):
            self.path.append(vertex1)


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []


    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.id not in self.vertices:
            self.vertices[vertex.id] = vertex
            return True
        else:
            return False


    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices and vertex2 in self.vertices:
            self.vertices[vertex1].add_neighbour(vertex2)
            self.vertices[vertex2].add_neighbour(vertex1)
            self.edges.append(Edge(vertex1, vertex2))
            return True
        else:
            return False


    def get_vertices(self):
        return self.vertices.keys()

    def get_edges(self):
        return [edge.vertices for edge in self.edges]

    def list_graph(graph):
        pass


    def __iter__(self):
        return iter(self.vertices.values())
