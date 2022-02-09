from .formatter import LinealOptimizationProblem
import numpy as np

def get_dual_problem(pol: LinealOptimizationProblem):
    ctx = [bj for _, bj in pol.b]
    Ax = np.transpose(np.array(pol.Ax))
    b = [('>=', cj) for cj in pol.ctx]
    return LinealOptimizationProblem('max', ctx, Ax, b)

