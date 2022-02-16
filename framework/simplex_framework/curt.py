import numpy as np
from explicit_form import find_canonic_base, get_base_of

def zp(x):
    if x > 0: return int(x)
    if int(x) > x: return int(x) - 1
    return x

def f(simplex, i, j):
    row = simplex.get_rows(i)
    y = row[j]
    return ( zp(y) - y ) * -1

# ( zp(y) - y ) * -1
def plane_cut_row_selection(simplex, formule):
    y = simplex.solution
    result = [(formule(y), None)]
    for i in range(len(simplex.Ax)):
        result.append(formule(simplex.y0[i]))
    
    result.sort()
    return result[0][1]

def cut_plane(simplex, i, formule ,*not_z_index):
    if i == None: y = simplex.solution
    else: y = simplex.y0[i]

    fio = formule(y)
    result = []
    for j in range(simplex.Ax[0]):
        if j in simplex.xb: result.append(0.0) 
        elif not j in not_z_index: result.append(formule(simplex.Ax[i][j]))
        elif simplex.Ax[i][j] >= 0: result.append(simplex.Ax[i][j])
        else: result.append((-1* fio/(1-fio)) * simplex.Ax[i][j])
    
    return result, '>=', fio


def cut_plane_z(simplex, r):
    rk = min([ rj for rj in simplex.rj if not rj == 0 ])
    row = simplex.Ax[r]
    Rr = [ i  for i in range(row.len) if row[i] < 0]
    Mj = [ -zp(simplex.r[i]/ rk) for i in Rr ]
    h = min([ mj/row[j] for mj, j in zip(Mj, Rr) ])
    
    result = []
    for j in range(len(simplex.Ax[0])):
        if j in simplex.base: result.append(0.0) 
        else: result.append(zp(h*row[j]))
    
    return result, '>=', zp(h*simplex.y0[r])

def cut_primal_z(simplex, k):
    _, r = min([ (simplex.y0[i]/row[k], i) for i, row in enumerate(simplex.Ax) if row[k] >= 1])
    row = simplex.Ax[r]
    yrk = row[k]
    result = []
    for j in range(len(simplex.Ax[0])):
        if j in simplex.base: result.append(0.0) 
        else: result.append(zp(row[j]/yrk))
    
    return result, '>=', zp(simplex.y0[r]/yrk)

def include_row(simplex, row, simbol, result):
    if simbol in ['<=', '<']:
        result = result * -1
        row = np.array(row) * -1

    simplex.Ax.append(row)
    simplex.y0.append(result)
    simplex.base = get_base_of(simplex.Ax, find_canonic_base(simplex.Ax))
    return simplex
