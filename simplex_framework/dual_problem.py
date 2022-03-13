from .formatter import LinealOptimizationProblem
import numpy as np
from .sale import check_sale

@check_sale
def get_dual_problem(pol: LinealOptimizationProblem):
    ctx = [bj for _, bj in pol.b]
    Ax = np.transpose(np.array(pol.Ax))
    b = [('<=', cj) for cj in pol.ctx]
    return LinealOptimizationProblem('max', ctx, Ax, b)

@check_sale
def is_dual_faceable(simplex):
    for item in simplex.y0:
        if item < 0: return False

    return True

# lambda rj, ypj : -rj/ypj
@check_sale
def dual_find_input_column(p, simplex, _min):
    if p is None: return None
    file_p = simplex.base.index(p)
    result = []
    for i in range(len(simplex.Ax[0])):
        if simplex.Ax[file_p][i] < 0 and simplex.rj[i] > 0:
            result.append((_min(simplex.rj[i], simplex.Ax[file_p][i]), i))

    result = [item for item in  result if not item[0] is None]

    if not any(result): return None
    result.sort()
    return result[0][1]

@check_sale
def dual_find_output_column(simplex):
    result = [(y0, i) for  i, y0 in enumerate(simplex.y0) if y0 < 0]
    if not any(result): return None
    result.sort()
    return simplex.base[result[0][1]]

