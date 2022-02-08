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