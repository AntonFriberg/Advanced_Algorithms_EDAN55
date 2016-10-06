import sys
import os
import random

cwd = os.getcwd()  # Current working directory
path = os.path.join(cwd, "data", sys.argv[1])
f = open(path)
r = int(sys.argv[2])  # number of iterations

n = int(f.readline())
P = [[0] * n for _ in xrange(n)]  # n x n matrix with zeros
alpha = 0.85  # damping factor

#  Create Adjacency Matrix
for line in f:
    edges = [int(s) for s in line.split() if s.isdigit()]
    for i in xrange(0, len(edges), 2):  # [from, to, from, to ...]
        P[edges[i]][edges[i + 1]] += 1  # add one edge, from -> to

# print P

# P[i][j] = probability of going from i to j in one step
# P[i][j] = probability of following link + probability of random walk
for i in xrange(len(P)):
    e = sum(P[i])  # total edges from vertex i
    if e != 0:
        P[i] = map(lambda x: float(x) / e * alpha + (1 - alpha) / n, P[i])
    else:
        P[i] = [float(1) / n] * n  # if no edges to vertex same probability


def matrix_multiplication(m_a, m_b):
    # Does not work in Python 3 use list(zip(m_b)) instead of zip(*m_b)
    return [[sum(e_a * e_b for e_a, e_b in zip(r_a, c_b))
             for c_b in zip(*m_b)] for r_a in m_a]


# recursive method for computing A ^ r by squaring log(r) times when power of 2
def compute_by_squaring(m, x):
    if x == 1:
        return m
    if x & 1:
        return matrix_multiplication(m, compute_by_squaring(matrix_multiplication(m, m), x / 2))
    return compute_by_squaring(matrix_multiplication(m, m), x / 2)


P = compute_by_squaring(P, r)

print(P[0])
