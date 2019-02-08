# Reads a coordinate file and parses the results into an array of coordinates.
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from matplotlib.collections import LineCollection
from scipy import spatial
import time

FILENAME = "SampleCoordinates.txt"
START_NODE = 0
END_NODE = 5
RADIUS = 0.08


def mercator_projection(a, b):

    r = 1
    x = r * np.pi * b / 180
    y = r * np.log(np.tan(np.pi / 4 + np.pi * a / 360))
    return x, y


def read_coordinate_file(filename):

    coords = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip('{}\n').split(sep=',')
            a = float(line[0])
            b = float(line[-1])
            coord = mercator_projection(a, b)
            coords.append(coord)

    return np.array(coords)


def plot_points(coord, indices, path):

    fig = plt.figure()
    ax = fig.gca()

    for i in range(7):
        plt.text(coord[i, 0] + .005, coord[i, 1], str(i))

    city_connections = coord[indices]
    cheapest_route = np.array([coord[i] for i in path])

    line_segments = LineCollection(city_connections, colors='grey', linewidths=0.5)

    ax.plot(cheapest_route[:, 0], cheapest_route[:, 1], 'b', linewidth=1)
    ax.plot(coord[:, 0], coord[:, 1], 'r.', markersize=3)
    ax.add_collection(line_segments)
    ax.autoscale(enable=True)

    plt.show()


def construct_graph_connections(coord, radius):
    cost = []
    city_connections = []

    for start, start_coord in enumerate(coord):
        for start_2, next_coord in enumerate(coord[start + 1:], start + 1):
            distance = np.linalg.norm(start_coord - next_coord)
            if distance <= radius:
                cost.append(np.power(distance, 9/10))
                city_connections.append([start, start_2])
    np_cost = np.array(cost)
    np_connections = np.array(city_connections)
    print(np_connections)
    print(cost)
    return np_connections, np_cost


def construct_fast_graph_connections(coord, radius):
    tree = spatial.cKDTree(coord)
    # Finds all neighbors within radius for
    b = tree.query(coord, radius)
    a = tree.query_ball_point(coord, radius)
    print(a)


def construct_graph(indices, costs, N):

    i = indices[:, 0]
    j = indices[:, 1]
    data = costs

    graph = csr_matrix((data, (i, j)), shape=(N, N))
    # print(graph)

    return graph


def cheapest_path(sparse_matrix, start):

    distance, predecessor = dijkstra(csgraph=sparse_matrix, directed=False, indices=start, return_predecessors=True)
    # print(distance)
    # print(predecessor)
    return distance, predecessor


def compute_path(predecessor, start_node, end_node):

    current_pos = end_node
    path = [end_node]

    while current_pos != start_node:
        current_pos = predecessor[current_pos]
        path.append(current_pos)
    # print("The cheapest path: ", path[::-1])
    return path[::-1]




coord_list = read_coordinate_file(FILENAME)
connections, travel_cost = construct_graph_connections(coord_list, RADIUS)
construct_fast_graph_connections(coord_list, RADIUS)
# N = numbers of cities
constructed_graph = construct_graph(connections, travel_cost, N=len(coord_list))
dist_matrix, predecessor_matrix = cheapest_path(constructed_graph, START_NODE)
calculated_path = compute_path(predecessor_matrix, START_NODE, END_NODE)
plot_points(coord_list, connections, calculated_path)
