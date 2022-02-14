from select import select
from unittest import result
import numpy as np
from pyparsing import java_style_comment

from simplex_framework.formatter import LinealOptimizationProblem
from .simplex import Simplex 
# from scipy.linalg import lu

# print(A)
# # A = np.array([[1,2,3], [2,4,2]])
# U = lu(A)[2]
# print(U)
# print(U.shape)
# li_columns = [np.flatnonzero(U[i :])[0] for i in range(U.shape[0])]
# print(li_columns)

def get_all_sub_set_with(elementAccount):
    result = []
    for n in range(2 ** elementAccount):
        result.append([i for i in range(elementAccount) if 1 << i & n != 0])

    return result

def get_base_of(pol, sub_base):
    all_sub_set = get_all_sub_set_with(len(pol.Ax[0]))

    def select(indexes):
        if len(indexes) != len(pol.Ax[0]): False
        for i in sub_base:
            if not i in indexes: False
        return True

    for indexes in [l for l  in all_sub_set if select(l)]:
        if is_base(indexes, pol): return indexes

    return []

def not_negative_base_vectors(pol, base):
    new_matrix, new_b = [], []

    for i, row in enumerate(pol.Ax):
        temp = 0
        for j in base:
            temp += row[j]
        if temp < 0:
            new_matrix.append(np.array(row) * -1)
            new_b.append((pol.b[i][0], pol.b[i][1] * -1))
        else :
            new_matrix.append(np.array(row))
            new_b.append(pol.b[i])

    return LinealOptimizationProblem(pol.verb, pol.ctx, new_matrix, new_b)

def get_canonical_columns(pol):
    matrix = pol.Ax
    vectors = {}
    for j in range(len(matrix[0])):
        resultOr = 0
        resultSum = 0
        index = -1
        for i, row  in enumerate(matrix):
            resultOr |= abs(row[j])
            resultSum += abs(row[j])
            index = i if abs(row[j]) == 1 else index
      
        if resultOr == resultSum == 1: 
            vectors[index] = j
    
    return [val for val in vectors.values()]

def is_base(indexes, pol):
    if len(indexes) != len(pol.Ax): return False

    newMatrix = []
    for row in pol.Ax:
        newMatrix.append([v for i, v in enumerate(row) if i in indexes])
    A = np.array(newMatrix)
    det = np.linalg.det(A)

    return not det == 0 

def completed_canonical_base(pol, canonical_columns):
    vector = []
    ctx = [0] * len(pol.ctx)
    for j in canonical_columns:
        ctx[j] = pol.ctx[j]
        for i, row in enumerate(pol.Ax):
            if row[j] == 1: vector.append(i)
    
    for i in range(len(pol.Ax)):
        if not i in vector: 
            ctx.append(1)
            canonical_columns.append(len(ctx)-1)
            for j, row in enumerate(pol.Ax):
                row.append(1 if i == j else 0)
    pol.ctx = ctx
    return pol, canonical_columns


#no utilizado 
def iscannon_Matrix(Matrix):
    uno =False
    sect = []
    for fila in Matrix:
        uno=False
        for i in range(len(fila)):
            if(fila[i]==1 and not uno):
                sect.append(i)
                uno=True
                continue
            if(fila[i]==1 and uno) :
                return False

            if (not (fila[i]==0)):
                return False

    for i in range(len(Matrix[0])) :
        if not (i in sect)  :
            return False                


    return True



def explicit_descompose(pol, base):
    xb = np.array([v for i, v in enumerate(pol.ctx) if i in base])
    xr = np.array([v for i, v in enumerate(pol.ctx) if not i in base])

    B, R = [], []
    for row in pol.Ax:
        B.append([v for i, v in enumerate(row) if i in base])
        R.append([v for i, v in enumerate(row) if not i in base])
    
    return Operator(xb), Operator(xr), Operator(np.array(B)), Operator(np.array(R))


def try_value(obj):
    try:
        return obj.value
    except AttributeError:
        return obj
        
class Operator:
    def __init__(self, value) -> None:
        self.value = value
    
    def __rmul__(self, other):
        return Operator(self.value.dot(try_value(other)))
    
    def __mul__(self, other):
        return Operator(self.value.dot(try_value(other)))
        
    def __add__(self, other): 
        return Operator(self.value + (try_value(other)))
        

    def __radd__(self, other): 
        return Operator(self.value + try_value(other))

    def __str__(self) -> str:
        return str(self.value)

    def __getitem__(self, index):
        return self.value[index]

def inverse_matrix(m):
    return Operator(np.linalg.inv(try_value(m)))

def simplex_build(base, ctb, ctr, B, R, y0, rj) -> None:
    self_ctb = try_value(ctb)
    self_ctr = try_value(ctr)
    self_B = try_value(B)
    self_R = try_value(R)
    self_y0 = try_value(y0)
    self_rj = try_value(rj)
    self_Ax = [[] for _ in base]
    self_ctx = []

    b_index = 0
    r_index = 0
    for i in range(len(rj)):
        if i in base:
            self_ctx.append(self_ctb[b_index])
            for j, row in enumerate(self_B):
                self_Ax[j].append(row[b_index])
            b_index += 1
        else:
            self_ctx.append(self_ctr[r_index])
            for j, row in enumerate(self_R):
                self_Ax[j].append(row[r_index])
            r_index += 1
    return Simplex(base, self_ctx, self_Ax, self_y0, self_rj)

