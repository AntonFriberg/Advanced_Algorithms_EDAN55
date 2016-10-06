import sys
import os
import random

cwd = os.getcwd()  # Current working directory
path = os.path.join(cwd, "data", sys.argv[1])
f = open(path)
iterations = int(sys.argv[2])  # number of iterations

n = int(f.readline())
G = [[] for _ in xrange(n)]

for line in f:
    edges = [int(s) for s in line.split() if s.isdigit()]
    for i in xrange(0, len(edges), 2):  # [from, to, from, to ...]
        G[edges[i]] += [edges[i + 1]]

print G

alpha = 0.85  # damping factor
visits = [0] * n
pos = 0
for i in xrange(iterations):
    visits[pos] += 1
    if len(G[pos]) != 0 and random.random() < alpha:
        pos = G[pos][random.randint(0, len(G[pos]) - 1)]
    else:
        pos = random.randint(0, n - 1)

rf = map(lambda x: float(x) / iterations * 100, visits)
print rf
