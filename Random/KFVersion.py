# Reads a coordinate file and parses the results into an array of coordinates.
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


def read_coordinate_file(filename):

    file = open(filename, "r")

    r = 1
    x, y = [], []

    for line in file:
        line = line.strip('{}\n').split(sep=',')
        a = float(line[0])
        b = float(line[-1])
        x.append(r * np.pi * b/180)
        y.append(r*np.log(np.tan(np.pi/4 + np.pi*a/360)))
    coordinates = np.column_stack((x, y))
    # print(coordinates)
    file.close()
    return coordinates


def plot_points(coord):
    plt.plot(coord[:, 0], coord[:, 1], 'o')
    plt.show()


def construct_graph_connections(coord, radius):
    cost = []
    node1, node2 = [], []
    for start, start_coord in enumerate(coord):
        for next_coord in range(start + 1, len(coord)):
            distance = np.linalg.norm(start_coord - coord[next_coord])
            if distance <= radius:
                cost.append(np.power(distance, 9/10))
                node1.append(start)
                node2.append(next_coord)
    np_cost = np.column_stack(cost)
    node_stack = np.column_stack((node1, node2))
    print(node_stack)
    return node_stack, np_cost

coord_list = read_coordinate_file("SampleCoordinates.txt")
plot_points(coord_list)
indices, travel_cost = construct_graph_connections(coord_list, 0.08)
# construct_graph(dist_cost[:, 0], dist_cost[:, 1], N=2) # N equals rows