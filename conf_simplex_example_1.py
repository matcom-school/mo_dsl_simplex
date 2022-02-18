import simplex_framework as mo

x, eq  = mo.format_componet(look=True)

eq.min_z = 2 * x[0] + 1 * x[1] + 3 * x[2] + 2 *x[3] +1* x[4]
eq.s_a = ( 
        1 * x[0] + 1 * x[1] + 1 * x[2] + 1* x[3] == 9,
        -1 * x[0] + 1 * x[1] + 2 * x[2] + 1 * x[4] == 3
    ) 


stand_eq = mo.get_stand_form(eq, look=True)
print(stand_eq)
base = mo.get_canonical_columns(stand_eq)

ctb, ctr, B, R = mo.explicit_descompose(stand_eq, base)
y0 = mo.inverse_matrix(B) * stand_eq.result_vector
ztr = ctb * mo.inverse_matrix(B) * R
rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in stand_eq.list_var_index_by(base) ]

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
