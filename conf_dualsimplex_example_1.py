import simplex_framework as mo

x, eq  = mo.format_componet()

eq.min_z = 3 * x[0] + 2 * x[1] + 1 * x[2] 
eq.s_a = ( 
        1 * x[0] + 1 * x[1] - 1 * x[2] >= 5,
        -2 * x[0] - 1 * x[1] + 2 * x[2] >= 4
    ) 


stand_eq = mo.get_stand_form(eq)
print(stand_eq)
base = mo.get_canonical_columns(stand_eq)
no_neg_eq = mo.not_negative_base_vectors(stand_eq, base)
print(no_neg_eq)

ctb, ctr, B, R = mo.explicit_descompose(no_neg_eq, base)
y0 = mo.inverse_matrix(B) * no_neg_eq.result_vector
ztr = ctb * mo.inverse_matrix(B) * R
rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in no_neg_eq.list_var_index_by(base) ]

simplex_to_eq = mo.simplex_build(base, ctb, ctr, B, R, y0, rj)
print(simplex_to_eq)

while not mo.is_dual_faceable(simplex_to_eq):
    ap = mo.dual_find_output_column(simplex_to_eq)
    aq = mo.dual_find_input_column(ap, simplex_to_eq, _min = lambda rj, ypj: -rj/ypj if ypj < 0 else None)

    if aq is None: 
        print("Problema no acotado") 
        break

    print("->",aq,'->', ap)
    ap = simplex_to_eq.base.index(ap)
    ypq = simplex_to_eq.Ax[ap][aq]
    simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq, 
        formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)
 
    print(simplex_to_eq)

  
print("Final result: ", mo.get_solution(simplex_to_eq))
