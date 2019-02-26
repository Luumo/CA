"""
creates cheapest path represented by a distance matrix with cost of travel between nodes,
and predecessor with cheapest path.

:param sparse_graph: sparse matrix [i, j], representing cost of route between i and j
:param start_node: starting node, which the path should be computed for
:return: distance as a  matrix with cheapest distance from node i, to node j through the graph,
        predecessor as a matrix [i,j] of the shortest paths from point i. Each index  in predecessor[i,j] consists
         previous node which was passed when traveling from the start node i to node j through the graph.
"""
# csgraph=sparse_graph, where sparce graph represents costs between routes, as described in the documentation
# directed=false, since the shortest path can be found from node i -> j, and j -> i.
# return_predecessors=True, since we need to reconstruct the shortest path later on.