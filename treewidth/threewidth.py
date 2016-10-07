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


def independent(edge_set, graph_in):
    for vertex in edge_set:
        remaining_set = set(edge_set) - set([vertex])
        if remaining_set & set(graph_in[n]):  # if intersection between sets different then empty set
            return False
    return True


def max_sum(num_neighbors, t_t, t_b, e_set, vi):
    l1 = list()
    for v1 in num_neighbors:
        l2 = list()
        for v2 in t_t[v1]:
            size = t_t[v1][v2]
            if size > 0:  # not a connection
                v1_n_e = t_b[v1] & e_set  # intersection betwen v1's bag and e_set
                v2_n_v = v2 & t_b[vi]  # intersection between v2 and vertex's bag
                if v1_n_e == v2_n_v:
                    l2.append(size - len(v2 & e_set))
        if len(l2):
            l1.append(max(l2))
    return sum(l1)


if len(sys.argv) != 2:
    print('Usage: python lab5.py filename (w/o file extension)')
    sys.exit(0)

cwd = os.getcwd()  # current working directory
path = os.path.join(cwd, "data", sys.argv[1])
files = [open(path + '.gr'), open(path + '.td')]

# initialize data structures
G = dict()
t_bag = dict()
t_neighbors = defaultdict(list)
tree_t = dict()
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
            e1 = int(e[0])
            e2 = int(e[1])
            t_neighbors[e1].append(e2)
            t_neighbors[e2].append(e1)

# =================================================================
# Choose correct root (same can be used in T)
# Construct a list of our connections between the bags
# =================================================================
root = min(t_neighbors, key=lambda x: len(t_neighbors[x]))  # index of the vertex with fewest neighbors
marked = {v: False for v in t_neighbors}
con = list()
construct_connections(con, t_neighbors, root, marked)



# =================================================================
# Associate the topological ordering for each vertex in T
# =================================================================
for vertex in con:
    if len(t_neighbors[vertex]) and vertex != root:  # no children or root
        for edge_set in tree_t[vertex]:
            if independent(edge_set, G):
                tree_t[vertex][edge_set] = len(edge_set)
                # print('Bag: ' + str(vertex))
                # print tree_t[vertex]
    else:
        for edge_set in tree_t[vertex]:
            if independent(edge_set, G):
                tree_t[vertex][edge_set] = len(edge_set) + max_sum(t_neighbors[vertex], tree_t, t_bag, edge_set, vertex)

m = tree_t[root]
elems_of_max_set = max(m.items(), key=operator.itemgetter(1))[0] #
print elems_of_max_set
output = "Maximum Independent Set\n"
output += "Elements: "
for vertex in elems_of_max_set:
    output += str(vertex) + " "

print(output)
print("independence number: " + str(max(m.values())))

