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



# buscar columna de salida
# realizar cambie de dos columnas
# realizar cortes  

# DualSimplex y Doble Fase ??????