import sys
import os

cwd = os.getcwd()  # current working directory
path = os.path.join(cwd, "data", sys.argv[1])
f = open(path)
r = int(sys.argv[2])  # number of iterations

n = int(f.readline())
P = [[0] * n for _ in xrange(n)]  # n x n matrix with zeros
H = [[0] * n for _ in xrange(n)]
D = [[0] * n for _ in xrange(n)]
deg = [0] * n
alpha = 0.85  # damping factor

#  create adjacency matrix
for line in f:
    edges = [int(s) for s in line.split() if s.isdigit()]
    for i in xrange(0, len(edges), 2):  # [from, to, from, to ...]
        P[edges[i]][edges[i + 1]] += 1  # add one edge, from -> to
        deg[edges[i]] += 1  # add one to degree

for i in xrange(n):
    for j in xrange(n):
        if deg[i] > 0:
            H[i][j] = float(P[i][j]) / deg[i]
            D[i][j] = 0
        else:
            H[i][j] = 0
            D[i][j] = float(1) / n

# P[i][j] = probability of going from i to j in one step
# P[i][j] = probability of following link + probability of random walk
for i in xrange(n):
    for j in xrange(n):
        P[i][j] = alpha * (H[i][j] + D[i][j]) + (1 - alpha) / n


# standard matrix multiplication
def matrix_multiplication(m_a, m_b):
    # Does not work in Python 3 use list(zip(m_b)) instead of zip(*m_b)
    return [[sum(e_a * e_b for e_a, e_b in zip(r_a, c_b))
             for c_b in zip(*m_b)] for r_a in m_a]


def check_stability(l1, l2):
    c = [0] * len(l1)
    for x in xrange(len(l1)):
        if float(str(l1[x])[:6]) == float(str(l2[x])[:6]):
            c[x] = 1
    return not (0 in c)


# recursive method computing A ^ r by squaring log(r) times when power of 2
def compute_by_squaring(m, x):
    if x == 1:
        return m
    if x & 1:
        return matrix_multiplication(m, compute_by_squaring(matrix_multiplication(m, m), x / 2))
    return compute_by_squaring(matrix_multiplication(m, m), x / 2)


PthPower = compute_by_squaring(P, r)

print

print "P matrix formatted for Latex"
output = ""
for x in xrange(len(P)):
    x = ['{:.2f}'.format(i) for i in P[x]]
    for i in xrange(len(P)):
        output += x[i] + " & "
    output = output[:-2]
    output += "\\\\\n"

# print output

print "P^r matrix formatted for Latex"
output = ""
for x in xrange(len(PthPower)):
    x = ['{:.2f}'.format(i) for i in PthPower[x]]
    for i in xrange(len(PthPower)):
        output += x[i] + " & "
    output = output[:-2]
    output += "\\\\\n"
# print output

print "H matrix formatted for Latex"
output = ""
for x in xrange(len(H)):
    x = ['{:.2f}'.format(i) for i in H[x]]
    for i in xrange(len(H)):
        output += x[i] + " & "
    output = output[:-2]
    output += "\\\\\n"
# print output

print "D matrix formatted for Latex"
output = ""
for x in xrange(len(D)):
    x = ['{:.2f}'.format(i) for i in D[x]]
    for i in xrange(len(D)):
        output += x[i] + " & "
    output = output[:-2]
    output += "\\\\\n"
# print output
