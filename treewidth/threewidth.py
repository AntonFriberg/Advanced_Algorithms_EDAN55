import sys
import os
import operator
import time
from collections import defaultdict
from itertools import chain, combinations

print(len(sys.argv))
if len(sys.argv) != 2:
    print('Usage: python lab5.py filename (w/o file extension)')
    sys.exit(0)

cwd = os.getcwd()  # current working directory
path = os.path.join(cwd, "data", sys.argv[1])
files = [open(path + '.gr'), open(path + '.td')]

# initialize data structures
G = dict(list)
t_bag = dict(set)
t_neighbors = dict(list)
tree_t = dict(dict)


for line in files[0]:



def parse(files):
    # d = 'data/'
    g_rows = open(files[0]).read().split('\n')
    t_rows = open(files[1]).read().split('\n')
    G = dict(list)
    t_bag = dict(set)
    t_neighbors = dict(list)
    tree_t = dict(dict)
    g_nodes = ''
    for r in g_rows:
        if len(r) > 0:
            if r[0] == 'p':
                g_nodes = int(r.split()[2])
                for i in range(1, g_nodes + 1):
                    G[i] = []
            elif r[0] == 'c':
                pass
            else:
                edge = r.split()
                if int(edge[0]) > g_nodes or int(edge[1]) > g_nodes:
                    print('Invalid edge: ' + edge[0] + ' -> ' + edge[1])
                    sys.exit(0)
                G[int(edge[0])].append(int(edge[1]))
                G[int(edge[1])].append(int(edge[0]))
    bags = tw = ''
    for r in t_rows:
        if len(r) > 0:
            if r[0] == 's':
                bags = int(r.split()[2])
                tw = int(r.split()[3])

            elif r[0] == 'b':
                nodes = [int(n) for n in r.split()[1:]]
                s_set = frozenset(nodes[1:])
                tree_t[nodes[0]] = {k: 0 for k in powerset(s_set)}
                t_bag[nodes[0]] = s_set
            elif r[0] == 'c':
                pass
            else:
                edge = r.split()
                if int(edge[0]) > g_nodes or int(edge[1]) > g_nodes:
                    print('Invalid edge: ' + edge[0] + ' -> ' + edge[1])
                    sys.exit(0)
                t_neighbors[int(edge[0])].append(int(edge[1]))
                t_neighbors[int(edge[1])].append(int(edge[0]))

    root = min(t_neighbors, key=lambda x: len(t_neighbors[x]))
    visited = {k: False for k in t_neighbors}
    l = list()
    build_list(l, t_neighbors, root, visited)
    # print(l)
    # print(G)
    # print(independent(frozenset([1,3,5]), G))
    first = time.clock()
    run(t_bag, t_neighbors, tree_t, G, l)
    print((time.clock() - first))


def build_list(l, T_n, node, visited):
    if visited[node]:
        pass
    else:
        visited[node] = True
        for c in T_n[node]:
            build_list(l, T_n, c, visited)
        l.append(node)


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


def independent(s, G):
    for n in s:
        k = s - set([n])
        if k.intersection(set(G[n])):
            return False
    return True


def powerset(in_set):
    # print(in_set)
    res = list()
    for z in chain.from_iterable(combinations(in_set, r) for r in range(len(in_set) + 1)):
        res.append(frozenset(z))
    return res
