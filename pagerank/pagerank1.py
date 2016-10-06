import sys
import os
import random

cwd = os.getcwd()  # current working directory
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


def check_stability(l1, l2):
    c = [0] * len(l1)
    for x in xrange(len(l1)):
        if float(str(l1[x])[:6]) == float(str(l2[x])[:6]):
            c[x] = 1
    return not (0 in c)


alpha = 0.85  # damping factor
visits = [0] * n
pos = 0
stableIt = 0
result = [0] * n
for i in xrange(iterations):
    visits[pos] += 1
    if len(G[pos]) != 0 and random.random() < alpha:
        pos = G[pos][random.randint(0, len(G[pos]) - 1)]
    else:
        pos = random.randint(0, n - 1)
    stableIt += 1
    temp = map(lambda x: float(x) / stableIt, visits)
    if check_stability(temp, result):
        break
    else:
        result = temp

print result
print stableIt
