import simplex_framework as mo
from simplex_framework.simplex import try_delete_column

x, eq  = mo.format_componet()

eq.min_z = 4 * x[0] + 1 * x[1] + 1 * x[2]
eq.s_a = ( 
        2 * x[0] + 1 * x[1] + 2 * x[2] == 4,
        3 * x[0] + 3 * x[1] + 1 * x[2] == 3
    ) 


stand_eq = mo.get_stand_form(eq)
print(stand_eq)
base = mo.get_canonical_columns(stand_eq)

real_ctx = stand_eq.ctx

##### First Face
ff_eq, base = mo.completed_canonical_base(stand_eq, base)
print(ff_eq)
ctb, ctr, B, R = mo.explicit_descompose(ff_eq, base)
y0 = mo.inverse_matrix(B) * ff_eq.result_vector
ztr = ctb * mo.inverse_matrix(B) * R
rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in ff_eq.list_var_index_by(base) ]

simplex_to_eq = mo.simplex_build(base, ctb, ctr, B, R, y0, rj)
print(simplex_to_eq)
while not mo.check_optimal_condition(simplex_to_eq):
    aq = mo.find_input_column(simplex_to_eq)
    ap = mo.find_swap_column_to(aq, simplex_to_eq, _min = lambda yio, yiq: yiq/yio if yio > 0 else None)

    if ap is None: 
        print("Problema no acotado") 
        break

    print("swap: ->",aq,'->', simplex_to_eq.base[ap])

    deleteColumn = simplex_to_eq.base[ap]
    ypq = simplex_to_eq.Ax[ap][aq]
    simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq, 
        formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)

    simplex_to_eq = try_delete_column(deleteColumn, simplex_to_eq)
    print(simplex_to_eq)
 
  
#### Second Face
sf_eq = mo.LinealOptimizationProblem('min', real_ctx, simplex_to_eq.Ax, [(mo.EQUAL, y0) for y0 in simplex_to_eq.y0])
base = simplex_to_eq.base
y0 = simplex_to_eq.y0
ctb, ctr, B, R = mo.explicit_descompose(sf_eq, base)
ztr = ctb * mo.inverse_matrix(B) * R
rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in sf_eq.list_var_index_by(base) ]


simplex_to_eq = mo.simplex_build(base, ctb, ctr, B, R, y0, rj)
print(simplex_to_eq)
while not mo.check_optimal_condition(simplex_to_eq):
    aq = mo.find_input_column(simplex_to_eq)
    ap = mo.find_swap_column_to(aq, simplex_to_eq, _min = lambda yio, yiq: yiq/yio if yio > 0 else None)

    if ap is None: 
        print("Problema no acotado") 
        break

    print("->",aq,'->', simplex_to_eq.base[ap])

    ypq = simplex_to_eq.Ax[ap][aq]
    simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq, 
        formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)
    
    print(simplex_to_eq)

print("Final result: ", mo.get_solution(simplex_to_eq))
