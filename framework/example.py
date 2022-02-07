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
xb, xr, B, R = mo.explicit_descompose(stand_eq, base)

# y0 = np.linalg.inv(B).dot(stand_eq.result_vector)
# print(y0)
# print(B.dot(R))
# # this not now if has logic ???
# xb, xr, B, R = mo.get_explicit_var(Ax_stand, index_base = [])
# y0 = mo.inverse(B) * b
# Ax_B_explicit = xb + mo.inverse(B) * R * xr
# cambiar todos los valores a un obj con .value y mult override para mejorer las operaciones en el dsl


# crear una interface de Simplex
# chequear primal factible 
# chequear condición de optimalidad
# buscar columna de entrada
# buscar columna de salida
# realizar cambie de dos columnas
# realizar cortes  

# DualSimplex y Doble Fase ??????