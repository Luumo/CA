# Reads a coordinate file and parses the results into an array of coordinates.
# changes right here
# adding some more changes
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from matplotlib.collections import LineCollection


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


def plot_points(coord, indices):
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(coord[:, 0], coord[:, 1], '.')

    a = coord[indices]
    print(a)

    line_segments = LineCollection(a)
    ax.add_collection(line_segments)

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
    # print(np_connections)
    # print(cost)

    return np_connections, np_cost


def construct_graph(indices, costs, N):

    i = indices[:, 0]
    j = indices[:, 1]
    data = costs

    # MxN is the shape. So if we got 5 elements in costs, we need N=5
    matrix = csr_matrix((data, (i, j)), shape=(N, N))
    print(matrix)


coord_list = read_coordinate_file("SampleCoordinates.txt")
connections, travel_cost = construct_graph_connections(coord_list, 0.08)
plot_points(coord_list, connections)
construct_graph(connections, travel_cost, N=len(travel_cost))