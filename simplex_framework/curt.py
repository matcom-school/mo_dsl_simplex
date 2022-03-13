import numpy as np
from simplex_framework.explicit_form import get_base_of, get_canonical_columns
from simplex_framework.sale import check_sale

@check_sale
def zp(x):
    if x > 0: return int(x)
    if int(x) > x: return int(x) - 1
    return x

def f(simplex, i, j):
    row = simplex.get_rows(i)
    y = row[j]
    return ( zp(y) - y ) * -1

# ( zp(y) - y ) * -1
@check_sale
def plane_cut_row_selection(simplex, formule):
    y = simplex.solution
    result = [(formule(y), len(simplex.Ax))]
    for i in range(len(simplex.Ax)):
        result.append((formule(simplex.y0[i]), i ))
    

    result.sort()
    return result[0][1]

def real_row(i, simplex):
    if i == len(simplex.Ax):
        return simplex.rj + [simplex.solution]
    return [item for item in simplex.Ax[i]] + [simplex.y0[i]]

def real_value(i, j, simplex):

    return real_row(i, simplex)[j]

@check_sale
def cut_plane(simplex, i, formule ,*not_z_index):
    y = real_value(i, len(simplex.Ax[0]), simplex)
    fio = formule(y)
    result = []
    for j in range(len(simplex.Ax[0])):
        if j in simplex.base: result.append(0.0) 
        elif not j in not_z_index: 
            result.append(formule(real_value(i,j,simplex)))
        elif simplex.Ax[i][j] >= 0: 
            result.append(real_value(i,j,simplex))
        else: result.append((-1* fio/(1-fio)) * real_value(i,j,simplex))
    
    return result, '>=', fio

@check_sale
def cut_plane_z(simplex, r):
    rk = min([ rj for rj in simplex.rj if not rj == 0 ])
    row = real_row(r, simplex)
    Rr = [ i  for i in range(len(row) - 1) if row[i] < 0]
    
    Mj = [ -zp(simplex.rj[i]/ rk) for i in Rr ]
    h = min([ mj/row[j] for mj, j in zip(Mj, Rr) ])
    
    result = []
    for j in range(len(simplex.Ax[0])):
        if j in simplex.base: result.append(0.0) 
        else: result.append(zp(h*row[j]))
    
    return result, '>=', zp(h*simplex.y0[r])

@check_sale
def cut_primal_z(simplex, k):
    _, r = min([ (simplex.y0[i]/row[k], i) for i, row in enumerate(simplex.Ax) if row[k] >= 1])
    row = real_row(r, simplex)
    yrk = row[k]
    result = []
    for j in range(len(simplex.Ax[0])):
        if j in simplex.base: result.append(0.0) 
        else: result.append(zp(row[j]/yrk))
    
    return result, '>=', zp(simplex.y0[r]/yrk)

@check_sale
def include_row(simplex, row, simbol, result):
    if simbol in ['>=', '>']:
        result = result * -1
        row = np.array(row) * -1

    row = [item for  item in row ] + [1]

    simplex.ctx.append(0)
    simplex.Ax = np.array([[item for item in row] + [0] for row in simplex.Ax] + [row])
    simplex.y0.append(result)
    simplex.rj.append(0)
    simplex.base.append(len(simplex.ctx) - 1)
    return simplex


@check_sale
def all_in_Z(_list):
    for item in _list:
        if item - int(item) > 0.00001 or item < 0: return False
    
    return True