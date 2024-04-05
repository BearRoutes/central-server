from graphs import Graph, Vertex, Edge, Route

# Create a NREFFloor2Graph with 4 vertices and 5 edges
NREFFloor2Graph = Graph()

location = ""

with open('nreffloor2.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        vertex_array = line.strip().split(",")
        # print(vertex_array)
        vertex = Vertex(vertex_array[0], (float(vertex_array[1]),float(vertex_array[2])))
        # print(f"Coordinates:{vertex.coordinates}")
        NREFFloor2Graph.add_vertex(vertex)
        

# NREFFloor2Graph

# for vertex in NREFFloor2Graph:
#     print(vertex.id)

# print(NREFFloor2Graph.get_vertices())

NREFFloor2Graph.add_edge('2-118','2-117')
NREFFloor2Graph.add_edge('2-117','2-125')
NREFFloor2Graph.add_edge('2-125','2-127')
NREFFloor2Graph.add_edge('2-127','2-132')
NREFFloor2Graph.add_edge('2-132','AST-8')
NREFFloor2Graph.add_edge('AST-8','ELV-179')
NREFFloor2Graph.add_edge('AST-8','2-002ZZ')
NREFFloor2Graph.add_edge('2-002ZZ','STR-1')
NREFFloor2Graph.add_edge('AST-2-132','2-132')
NREFFloor2Graph.add_edge('AST-2-132','2-011')
NREFFloor2Graph.add_edge('2-011','STR-6')
NREFFloor2Graph.add_edge('STR-6','2-005ZZB')
NREFFloor2Graph.add_edge('2-005ZZB','ELV-18X')

# TO THE LEFT OF THE ELEVATOR 182
NREFFloor2Graph.add_edge('ELV-18X','2-005ZZA')
NREFFloor2Graph.add_edge('2-060C','2-005ZZA')
NREFFloor2Graph.add_edge('2-060C','2-060B')
NREFFloor2Graph.add_edge('2-060B','2-060A')
NREFFloor2Graph.add_edge('2-060A','STR-5')
NREFFloor2Graph.add_edge('STR-5','2-118')
NREFFloor2Graph.add_edge('2-060A','2-052')
NREFFloor2Graph.add_edge('2-052','2-043')
NREFFloor2Graph.add_edge('2-043','2-048')
NREFFloor2Graph.add_edge('2-043','2-047')
NREFFloor2Graph.add_edge('2-048','2-050')
NREFFloor2Graph.add_edge('2-047','2-042')
NREFFloor2Graph.add_edge('2-042','2-039')
NREFFloor2Graph.add_edge('2-039','2-038')
NREFFloor2Graph.add_edge('2-038','2-054')
NREFFloor2Graph.add_edge('2-054','2-090')
NREFFloor2Graph.add_edge('2-090','2-005ZZA')

# TO THE RIGHT OF ELEVATOR 180
NREFFloor2Graph.add_edge('2-005ZZB','STR-2')
NREFFloor2Graph.add_edge('STR-2','2-001ZZD')

# DOWN
NREFFloor2Graph.add_edge('2-001ZZD','2-010')
NREFFloor2Graph.add_edge('2-010','2-016')
NREFFloor2Graph.add_edge('2-016','2-020')
NREFFloor2Graph.add_edge('2-020','STR-3')

# UP
NREFFloor2Graph.add_edge('2-001ZZD','2-001ZZC')
NREFFloor2Graph.add_edge('2-001ZZC','2-001ZZB')
NREFFloor2Graph.add_edge('2-001ZZC','2-003')
NREFFloor2Graph.add_edge('2-001ZZB','2-001')
NREFFloor2Graph.add_edge('2-001ZZB','2-001ZZA')
NREFFloor2Graph.add_edge('2-001ZZA','Pedway')
NREFFloor2Graph.add_edge('2-001ZZB','2-002')
NREFFloor2Graph.add_edge('2-002','AST-2-132')

# for vertex in NREFFloor2Graph:
#     print(vertex.id)
#     print(vertex.neighbours)
# for edges in NREFFloor2Graph.get_edges():
#     print(edges)