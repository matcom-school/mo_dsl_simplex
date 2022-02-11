import simplex_framework as mo
import numpy as np

# x infinity list var
# min.z and max.z or max_z, min_z object that receive one lop from assing op
# sa or s.a set a tuple of inequality
# ctx is a lineal equation result of assign to min or max

# Axb is a matrix result of assing to s.a 


#Modificaciones en los metodos de sacar columna que entra a la base y la que sale 
#Modificaciones en cambiar las columnas
#Modificaciones a la hora de dar los resultados
#Eliminar el 2^n al generar todos los conjuntos de vectores a e cual es base 
#de Exixstir siempre una canonica se busca o se hace una trandformacion

x, eq  = mo.format_componet(look=True)

eq.min_z = 2 * x[0] + 1 * x[1] + 3 * x[2] + 2 *x[3] +1* x[4]


eq.s_a = ( 
       
       
        1 * x[0] + 1 * x[1] + 1 * x[2] + 1* x[3] == 9,
        -1 * x[0] + 1 * x[1] + 1 * x[2] + 1 * x[4] == 3
       
       
    ) 



stand_eq = mo.get_stand_form(eq, look=True)
#base  = mo.get_base_of(stand_eq.Ax)
base= mo.get_cannon_bas(stand_eq.Ax)

print("La base Canonica es " + str(base))

ctb, ctr, B, R = mo.explicit_descompose(stand_eq, base)


y0 = mo.inverse_matrix(B) * stand_eq.result_vector

ztr = ctb * mo.inverse_matrix(B) * R

rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in stand_eq.list_var_index_by(base) ]


simplex_to_eq = mo.simplex_build(base, ctb, ctr, B, R, y0, rj)

while mo.check_optimal_condition(simplex_to_eq):
    aq = mo.find_input_column(simplex_to_eq)
   
    ap = mo.find_swap_column_to(aq, simplex_to_eq, _min = lambda yio, yiq: yiq/yio if yio > 0 else None)
    
    

    if ap is None: 
        print("Problema no acotado") 
        break

    print("Entra a la base "  + str(aq))
    print("Sale de la base " + str (simplex_to_eq.base[ap]))

    ypq = simplex_to_eq.Ax[ap][aq]
    simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq, 
        formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)
 
  

print("Final result: ", mo.get_solution(simplex_to_eq))

# realizar cortes  
# DualSimplex y Doble Fase ??????