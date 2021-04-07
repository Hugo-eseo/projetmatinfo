from math import sqrt
import time

def det(m, n, p):
    # m, n, p tuples of 2
    det = m[0] * n[1] + m[1] * p[0] + n[0] * p[1]
    det -= m[1] * n[0] + m[0] * p[1] + n[1] * p[0]
    return det

def barycentre(A1, A2, B1, B2):
    # A1, A2, B1, B2 tuples of 2
    part1 = (det(B1, B2, A2) * A1[0], det(B1, B2, A2) * A1[1])
    part2 = (det(B2, B1, A1) * A2[0], det(B2, B1, A1) * A2[1])
    numerateur = (part1[0] + part2[0], part1[1] + part2[1])
    denominateur = det(B1, B2, A2) + det(B2, B1, A1)
    if denominateur == 0: return None
    I = (numerateur[0] / denominateur, numerateur[1] / denominateur)
    return I

def distance_two_points(a, b):
    # a, b tuples of 2
    part1 = b[0] - a[0]
    part2 = b[1] - a[1]
    dist = sqrt(part1**2 + part2**2)
    return dist

def find_direction(a, b):
    # a, b tuples of 2
    if a[0] > b[0]:
        if a[1] > b[1]:
            return "NO"
        elif a[1] < b[1]:
            return "SO"
        else:
            return "O"
    elif a[0] < b[0]:
        if a[1] > b[1]:
            return "NE"
        elif a[1] < b[1]:
            return "SE"
        else:
            return "E"
    else:
        if a[1] > b[1]:
            return "N"
        elif a[1] < b[1]:
            return "S"
        else:
            return None


if __name__ == '__main__':
    A1 = (-1, -1)
    A2 = (3, 1)
    B1 = (6, 0)
    B2 = (2, -2)
    t1 = time.time()
    print(distance_two_points(A1, B1))
    print(barycentre(A1, A2, B1, B2))   # ça fonctionne j'ai dessiné sur papier pour comparer
    t2 = time.time()
    print("temps d'execution", t2-t1, 'secondes')
