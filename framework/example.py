import simplex_framework as mo
import numpy as np

# x infinity list var
# min.z and max.z or max_z, min_z object that receive one lop from assing op
# sa or s.a set a tuple of inequality
# ctx is a lineal equation result of assign to min or max

# Axb is a matrix result of assing to s.a 

x, eq  = mo.format_componet(look=True)

eq.min_z = 3 * x[1] + 2 * x[3] - x[0]
eq.s_a = ( 
       3 * x[1] + 2 * x[3] - x[0] > 0,
       3 * x[1] + 2 * x[3] - x[0] < 0,
       3 * x[1] + 2 * x[3] - x[0] <= 0,
       3 * x[1] + 2 * x[3] - x[0] >= 0,
       3 * x[1] + 2 * x[3] - x[0] == 1 
    ) 

stand_eq = mo.get_stand_form(eq, look=True)
base  = mo.get_base_of(stand_eq.Ax)
ctb, ctr, B, R = mo.explicit_descompose(stand_eq, base)

y0 = mo.inverse_matrix(B) * stand_eq.result_vector
ztr = ctb * mo.inverse_matrix(B) * R
rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in stand_eq.list_var_index_by(base) ]


simplex_to_eq = mo.simplex_build(base, ctb, ctr, B, R, y0, rj)

while mo.check_optimal_condition(simplex_to_eq):
    aq = mo.find_input_column(simplex_to_eq)
    ap = mo.find_swap_column_to(aq, simplex_to_eq, _min = lambda yio, yiq: yio/yiq if yiq > 0 else None)
    if ap is None: 
        print("Problema no acotado") 
        break

    ypq = simplex_to_eq.Ax[ap][aq]
    simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq, 
        formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)


print("Final result: ", mo.get_solution(simplex_to_eq))

# probar lo que hay
# leer dualSimplex y Doble fase y cortes 
# buscar columnas canonicas y annadir las faltantes y devolver la base
# realizar cortes  
# DualSimplex y Doble Fase ??????