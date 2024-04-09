# from nref_floor2_graph import NREFFloor2Graph

# Sources: https://favtutor.com/blogs/breadth-first-search-python


from nref_floor2_graph import NREFFloor2Graph

class Route:
    def __init__(self):
        self.graph = NREFFloor2Graph

    def bfs_route(self, start, goal):
        # Check if the start node is the goal node
        if start == goal:
            return [start]

        # Initialize a queue with the starting node and the path (just the start node)
        queue = [(start, [start])]
        visited = set()  # Set to keep track of visited nodes

        while queue:
            # Get the next node and path from the queue
            current_node, path = queue.pop(0)

            # Add the current node to the visited set
            visited.add(current_node)

            # Explore each neighbor of the current node
            for neighbour in self.graph.vertices[current_node].neighbours:
                if neighbour == goal:
                    route = path + [neighbour]
                    return route  # Return the path including the goal
                if neighbour not in visited:
                    # Add the neighbor to the queue with the updated path
                    queue.append((neighbour, path + [neighbour]))
                    # Add neighbor to visited to prevent revisiting
                    visited.add(neighbour)

        # Return an empty list if no path is found
        return []

# Example usage
# route = Route()
# print(route.bfs_route('2-118','2-042'))

# NREFFloor2Graph.vertices['2-118'].increase_heat()
# NREFFloor2Graph.vertices['2-118'].increase_heat()
# heat = NREFFloor2Graph.vertices['2-118'].heat_level
# print(heat)

# # Increase heat of nodes in the final path
# # In future iterations, heat will help determine optimal routes
# for node in route:
#     self.graph.vertices[node].increase_heat()
