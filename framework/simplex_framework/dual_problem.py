from unittest import result
from .formatter import LinealOptimizationProblem
import numpy as np

def get_dual_problem(pol: LinealOptimizationProblem):
    ctx = [bj for _, bj in pol.b]
    Ax = np.transpose(np.array(pol.Ax))
    b = [('<=', cj) for cj in pol.ctx]
    return LinealOptimizationProblem('max', ctx, Ax, b)


# lambda rj, ypj : -rj/ypj
def dual_find_input_column(p, simplex, formule):
    if p is None: return None

    result = []
    for i in range(len(simplex.Ax[0])):
        if simplex.Ax[p][i] < 0 and simplex.rj[i] > 0:
            result.append((formule(simplex.rj[i], simplex.Ax[p][i]), i))

    if not any(result): return None
    result.sort()
    return result[0][1]

def dual_find_output_column(simplex):
    result = [(y0, i) for  i, y0 in simplex.y0 if y0 < 0]
    if not any(result): return None
    result.sort()
    return simplex.base[result[0][1]]


def dual_eval(dual, sol):
    result = 0
    for i, s in enumerate(sol):
        result += dual.func_obj[i] * s
    return result