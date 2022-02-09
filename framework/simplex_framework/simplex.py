from typing import List
from unittest import result
import numpy as np

class Simplex:
    def __init__(self, base, ctx, Ax, y0, rj) -> None:
        self.base = base
        self.ctx = ctx
        self.Ax = np.array(Ax)
        self.y0 = y0
        self.rj = rj


def check_optimal_condition(simplex):
    for rj in simplex.rj:
        if rj < 0: return False
    
    return True

def check_primal_feasible(simplex):
    for y0 in simplex.y0:
        if y0 < 0: return False

    return True

def find_input_column(simplex):
    result = []
    for i, rj in enumerate(simplex.rj):
        if not i in simplex.base and rj < 0:
            result.append((rj, i))
    
    if not any(result): return None

    result.sort()
    return result[0][1] 

def find_swap_column_to(q, simplex, _min):
    if q is None: return None
    resultList = [(i, _min(simplex.Ax[i][q], simplex.y0[i])) for i in range(len(simplex.base)) ]
    resultList = [item for item in  resultList if not item[1] is None]

    if not any(resultList): return None 
    print(resultList) 
    resultList.sort(key= lambda x: x[1])
    return resultList[0][0]
 

def swap_column_base(q, p, simplex, formule):
    new_matrix = [[] for _ in range(len(simplex.base))]

    for i, row in enumerate(simplex.Ax):
        for j, item in enumerate(row):
            new_matrix[i].append(formule(i, j, item, simplex.Ax[i][q], simplex.Ax[p][j]))
    
    new_y0 = []
    for i, item in enumerate(simplex.y0):
        new_y0.append(formule(i, len(simplex.Ax[0], item, simplex.Ax[i][q], simplex.y0[p])))
    
    new_rj = []
    for j, item in enumerate(simplex.rj):
        new_rj.append(formule(len(simplex.Ax), j, item, simplex.rj[q], simplex.Ax[p][j]))
    
    simplex.base.remove(p)
    simplex.base.append(q)
    return Simplex(simplex.base, simplex.ctx, new_matrix, new_y0, new_rj)

def get_solution(simplex):
    result = [ 0 ] * len(simplex.Ax[0])
    for j in simplex.base:
        for row in simplex.Ax:
            if row[j] != 0:
                result[j] = row[j] * simplex.y0[j]

    return result