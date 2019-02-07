def plot_points(coord, indices, path):
    # print(coord, '\n', path, '\n', indices)
    fig = plt.figure()
    ax = fig.gca()
    # dots
    ax.plot(coord[:, 0], coord[:, 1], '.', 'r')
    # lines
    a = coord[indices]
    # print(a)

    b = [coord[i] for i in path]
    print(b)
    c = np.array(b)
    ax.plot(c[:, 0], c[:, 1], 'b')
    print(c)
    segment = np.array([c[:, 0], c[:, 1]])
    print(segment)
    line_segments = LineCollection(a, colors='grey')
    ax.add_collection(line_segments)