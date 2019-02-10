# Reads a coordinate file and parses the results into an array of coordinates.
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from matplotlib.collections import LineCollection
from scipy import spatial
import time

# initial values
FILENAME = "SampleCoordinates.txt"
START_NODE = 0
END_NODE = 5
RADIUS = 0.08


def mercator_projection(latitude, longitude):

    r = 1
    x = r * np.pi * longitude / 180
    y = r * np.log(np.tan(np.pi / 4 + np.pi * latitude / 360))
    return x, y


def read_coordinate_file(filename):

    coordinates = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip('{}\n').split(sep=',')
            latitude = float(line[0])
            longitude = float(line[-1])
            coord = mercator_projection(latitude, longitude)
            coordinates.append(coord)

    return np.array(coordinates)


def plot_points(coord_list, indices, path):

    fig = plt.figure()
    ax = fig.gca()

    city_connections = coord_list[indices]
    cheapest_route = coord_list[path]

    line_segments = LineCollection(city_connections, colors='grey', linewidths=0.5)

    ax.plot(cheapest_route[:, 0], cheapest_route[:, 1], 'b', linewidth=1)
    ax.plot(coord_list[:, 0], coord_list[:, 1], 'r.', markersize=3)  # dotted cities
    ax.add_collection(line_segments)



    plt.show()


def construct_graph_connections(coord_list, radius):
    # Computes all connections between all points in coord_list within radius
    # Returns: Connections between all neighbouring cities and the cost of traveling between these cities

    cost = []
    city_connections = []

    for start, start_coord in enumerate(coord_list):
        for end in range(start + 1, len(coord_list)):
            next_coord = coord_list[end]
            distance = np.linalg.norm(start_coord - next_coord)
            if distance <= radius:
                cost.append(np.power(distance, 9/10))
                city_connections.append([start, end])
    np_cost = np.array(cost)
    np_connections = np.array(city_connections)

    return np_connections, np_cost


def construct_fast_graph_connections(coord_list, radius):

    tree = spatial.cKDTree(coord_list)
    # returns a list of neighbors within the given radius of each node.
    start_ends = tree.query_ball_point(coord_list, radius)

    city_connections, cost = [], []
    # removing city connection doublets
    for start, ends in enumerate(start_ends):
        for end in ends:
            if start < end:
                distance = np.linalg.norm(coord_list[start] - coord_list[end])
                city_connections.append([start, end])
                cost.append(np.power(distance, 9/10))

    np_connections = np.array(city_connections)
    np_cost = np.array(cost)

    return np_connections, np_cost


def construct_graph(indices, costs, N):

    i = indices[:, 0]
    j = indices[:, 1]
    data = costs

    # At [i,j] in the sparse matrix, the cost of this route between i and j can be found.
    graph = csr_matrix((data, (i, j)), shape=(N, N))    # N is equal to amount of cities in coord_list
    return graph


def cheapest_path(sparse_graph, start_node):
    # Returns a matrix with cheapest distance from node i, to node j through the graph.
    # Predecessor returns a list of the shortest paths from point i. Each following index consists previous node
    # which was passed when traveling from the start node i to node j through the graph.

    distance, predecessor = dijkstra(csgraph=sparse_graph, directed=False, indices=start_node, return_predecessors=True)
    return distance, predecessor


def compute_path(predecessor, start_node, end_node):

    current_pos = end_node
    path = [end_node]

    # computes path by going through predecessor list from end node until start_node has been found
    while current_pos != start_node:
        current_pos = predecessor[current_pos]
        path.append(current_pos)
    print("The cheapest path from {} to {}: {}".format(start_node, end_node, path[::-1]))

    return path[::-1]


def print_cost_cheapest_path(dist, end_node):
    total_cost = dist[end_node]
    print("Total Cost: {}".format(total_cost))


coordinate_list = read_coordinate_file(FILENAME)

# connections, travel_cost = construct_graph_connections(coordinate_list, RADIUS)
connections, travel_cost = construct_fast_graph_connections(coordinate_list, RADIUS)

constructed_graph = construct_graph(connections, travel_cost, N=len(coordinate_list))
dist_matrix, predecessor_matrix = cheapest_path(constructed_graph, START_NODE)
print_cost_cheapest_path(dist_matrix, END_NODE)
calculated_path = compute_path(predecessor_matrix, START_NODE, END_NODE)
plot_points(coordinate_list, connections, calculated_path)