from typing import List
from unittest import result
import numpy as np
from simplex_framework.prettier_print import print_number

class Simplex:
    def __init__(self, base, ctx, Ax, y0, rj) -> None:
        self.base = base
        self.ctx = ctx
        self.Ax = np.array(Ax)
        self.y0 = y0
        self.rj = rj

    def __str__(self) -> str:
        result = f'actual base: {self.base}\n'
        result += print_list(self.ctx) + ' |\n'
        for i, row in enumerate(self.Ax):
            result += print_list(row) + f' | {print_number(self.y0[i])}\n'

        return result + print_list(self.rj) + f' | {print_number(get_solution(self)[1])}\n'



def print_list(listt):
    result = ''
    for i,n in enumerate(listt):
        result += print_number(n) 
        if i == len(listt): continue
        result += ','
    return result


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
    resultList.sort(key= lambda x: x[1])
    return resultList[0][0]
 

def swap_column_base(q, p, simplex, formule):
    new_matrix = [[] for _ in range(len(simplex.base))]

    for i, row in enumerate(simplex.Ax):
        for j, item in enumerate(row):
            new_matrix[i].append(formule(i, j, item, simplex.Ax[i][q], simplex.Ax[p][j]))
    
    new_y0 = []
    for i, item in enumerate(simplex.y0):
        new_y0.append(formule(i, len(simplex.Ax[0]), item, simplex.Ax[i][q], simplex.y0[p]))
    
    new_rj = []
    for j, item in enumerate(simplex.rj):
        new_rj.append(formule(len(simplex.Ax), j, item, simplex.rj[q], simplex.Ax[p][j]))
    
    simplex.base[(p)]=q
    return Simplex(simplex.base, simplex.ctx, new_matrix, new_y0, new_rj)


def get_solution(simplex):
    result = [ 0 ] * len(simplex.Ax[0])
    for j in range(len(simplex.base)):
        for row in simplex.Ax:
            if row[simplex.base[j]] != 0:
                result[simplex.base[j]] = 1 * simplex.y0[j]

    return result , evaluate(result,simplex)

def evaluate (result,simplex):
    z = 0
    for i in range(len(simplex.ctx)):
        z = z + simplex.ctx[i] * result[i]

    return z    

def try_delete_column(index, simplex):
    print("try delete", index)
    if not index in simplex.base:
        simplex.ctx.pop(index)
        new_matrix = []
        for row in simplex.Ax:
            try:
                row.pop(index)
                new_matrix.append(row)
            except AttributeError:
                new_matrix.append(np.delete(row, index))


        simplex.rj.pop(index)
        simplex.Ax = np.array(new_matrix)
    return simplex