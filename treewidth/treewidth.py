import sys
import os
import operator
import time
from collections import defaultdict
from itertools import chain, combinations


def powerset(iterable):
    " powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    res_sets = list()
    for s in chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1)):
        res_sets.append(frozenset(s))  # need frozenset to be hashable inside a dict
    return res_sets


def construct_connections(connections, t_in, vi, visited):
    if not visited[vi]:
        visited[vi] = True
        for v in t_in[vi]:
            construct_connections(connections, t_in, v, visited)
        connections.append(vi)


def independent(s, graph_in):
    for v_i in s:
        remaining_set = s - set([v_i])
        if remaining_set.intersection(set(graph_in[v_i])):  # if intersection between sets different then empty set
            return False
    return True


def set_manipulation(num_neighbors, t_t, t_b, in_set, vi):
    tl = list()
    for n in num_neighbors:
        ul = list()
        for ui in t_t[n]:
            size = t_t[n][ui]
            if size > 0:  # not any connection
                ui_vi = ui.intersection(t_b[vi])  # intersection betwen v1's bag and e_set
                in_n  = in_set.intersection(t_b[n])  # intersection between v2 and vertex's bag
                if ui_vi == in_n:
                    w = ui.intersection(in_set)
                    ul.append(size - len(w))
        if ul: tl.append(max(ul))
    return sum(tl)


def associate_topology(G, t_neighbors, tree_t, t_bag, con):
    # =================================================================
    # Associate the topological ordering for each vertex in T
    # =================================================================
    root = con[len(con) - 1]
    for vertex in con:
        if len(t_neighbors[vertex]) == 1 and vertex != root:  # no children or root
            for edge_set_s in tree_t[vertex]:
                if independent(edge_set_s, G):
                    tree_t[vertex][edge_set_s] = len(edge_set_s)
                    # print('Bag: ' + str(vertex))
                    # print tree_t[vertex]
        else:
            for edge_set_u in tree_t[vertex]:
                if independent(edge_set_u, G):
                    tree_t[vertex][edge_set_u] = len(edge_set_u) + set_manipulation(t_neighbors[vertex], tree_t, t_bag,
                                                                                    edge_set_u,
                                                                                    vertex)

    m = tree_t[root]
    elems_of_max_set = max(m.items(), key=operator.itemgetter(1))[0]  #
    print elems_of_max_set
    output = "Maximum Independent Set\n"
    output += "Elements: "
    for vertex in elems_of_max_set:
        output += str(vertex) + " "

    print(output)
    print("independence number: " + str(max(m.values())))


def parse_graph(files):
    # initialize data structures
    G = defaultdict(list)
    t_bag = defaultdict(set)
    t_neighbors = defaultdict(list)
    tree_t = defaultdict(dict)
    # =================================================================
    # Parse the graph G
    # =================================================================
    for line in files[0]:
        if len(line) > 0 and line[0] != 'c':
            if line[0] == 'p':
                n = int(line.split()[2])  # read number of nodes
                for i in xrange(1, n + 1):
                    G[i] = []
            else:
                e = line.split()
                G[int(e[0])].append(int(e[1]))
                G[int(e[1])].append(int(e[0]))

    # =================================================================
    # Parse the tree decomposition T as a graph
    # =================================================================
    for line in files[1]:
        if len(line) > 0 and line[0] != 'c':
            if line[0] == 's':
                bags = int(line.split()[2])
                tw = int(line.split()[3])
            elif line[0] == 'b':
                vertices = [int(v) for v in line.split()[1:]]
                set_components = set(vertices[1:])
                t_bag[vertices[0]] = set_components
                tree_t[vertices[0]] = {v: 0 for v in powerset(set_components)}  # store the possible connections
            else:
                e = line.split()
                e0 = int(e[0])
                e1 = int(e[1])
                t_neighbors[e0].append(e1)
                t_neighbors[e1].append(e0)

    # =================================================================
    # Choose correct root (same can be used in T)
    # Construct a list of our connections between the bags
    # =================================================================
    root = min(t_neighbors, key=lambda x: len(t_neighbors[x]))  # index of the vertex with fewest neighbors
    marked = {v: False for v in t_neighbors}
    con = list()
    construct_connections(con, t_neighbors, root, marked)
    associate_topology(G, t_neighbors, tree_t, t_bag, con)


def main(args):
    if len(args) < 1:
        print('Wrong number of arguments')
        sys.exit(0)

    cwd = os.getcwd()  # current working directory
    path = os.path.join(cwd, "data", sys.argv[1])
    files = [open(path + '.gr'), open(path + '.td')]
    parse_graph(files)

if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    done = time.time()
    elapsed = done - start
    print(elapsed)