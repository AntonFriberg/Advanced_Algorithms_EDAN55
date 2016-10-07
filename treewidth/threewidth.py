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
        res_sets.append(frozenset(s)) # need frozenset to be hashable inside a dict
    return res_sets


def construct_connections(con, t_in, vertex, visited):
    if not visited[vertex]:
        visited[vertex] = True
        for v in t_in[vertex]:
            construct_connections(con, t_in, v, visited)
        con.append(vertex)


def independent(edge_set, graph_in):
    for vertex in edge_set:
        remaining_set = set(edge_set) - set([vertex])
        if remaining_set & set(graph_in[n]): # if intersection between sets different then empty set
            return False
    return True


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

for line in files[1]:
    if len(line) > 0 and line[0] != 'c':
        if line[0] == 's':
            bags = int(line.split()[2])
            tw = int(line.split()[3])
        elif line[0] == 'b':
            vertices = [int(v) for v in line.split()[1:]]
            set_components = set(vertices[1:])
            t_bag[vertices[0]] = set_components
            tree_t[vertices[0]] = {v:0 for v in powerset(set_components)}  # store the possible connections
        else:
            e = line.split()
            e1 = int(e[0])
            e2 = int(e[1])
            t_neighbors[e1].append(e2)
            t_neighbors[e2].append(e1)

root = min(t_neighbors, key=lambda x: len(t_neighbors[x]))  # index of the vertex with fewest neighbors
marked = {v: False for v in t_neighbors}
con = list()
construct_connections(con, t_neighbors, root, marked)

print con
print G


# root = con[len(con) - 1]
def maxsum(num_neighbors, tree_t, t_bag, e_set, vertex):
    l1 = list()
    for v1 in num_neighbors:
        l2 = list()
        for v2 in tree_t[v1]:
            size = tree_t[v2, v2]
            if size > 0: # not a connection
                v1_n_e = t_bag[v1] & e_set # intersection betwen v1's bag and e_set
                v2_n_v = v2 & t_bag[vertex] # intersection between v2 and vertex's bag
                if v1_n_e == v2_n_v:




def maxsum(ninjos, T_t, T_b, u, node):
    t_list = list()
    for n in ninjos:
        u_list = list()
        for ui in T_t[n]:
            size = T_t[n][ui]  # U_i
            if size > 0:  # independent
                ui_vt = ui.intersection(T_b[node])
                u_vn = u.intersection(T_b[n])
                if ui_vt == u_vn:
                    w = ui.intersection(u)
                    u_list.append(size - len(w))
        if u_list: t_list.append(max(u_list))
    return sum(t_list)


for vertex in con:
    if len(t_neighbors[vertex]) and vertex != root: # no children or root
        for edge_set in tree_t[vertex]:
            if independent(edge_set, G):
                tree_t[vertex][edge_set] = len(edge_set)
                #print('Bag: ' + str(vertex))
                #print tree_t[vertex]
    else:
        for edge_set in tree_t[vertex]:
            if independent(edge_set, G):
                tree_t[vertex, edge_set] = len(edge_set) + maxsum(t_neighbors[vertex], tree_t, t_bag, edge_set, vertex)










def run(T_b, treeNeighbors, T_t, G, l):
    root = l[len(l) - 1]
    for i in l:
        if len(treeNeighbors[i]) == 1 and i != root:  # Check for leaves
            for s in T_t[i]:
                if independent(s, G):
                    T_t[i][s] = len(s)
                    # print('Bag: ' + str(i))
                    # print(T_t[i])
        else:
            for u in T_t[i]:
                if independent(u, G):
                    T_t[i][u] = len(u) + maxsum(treeNeighbors[i], T_t, T_b, u, i)
    m = T_t[root]
    s = max(m.items(), key=operator.itemgetter(1))
    print(s)
    print(max(m.values()))




def independent(s, G):
    for n in s:
        k = s - set([n])
        if k.intersection(set(G[n])):
            return False
    return True
