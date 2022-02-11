import numpy as np
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

def find_canonic_base(matrix):
    result = []
    for j in range(len(matrix[0])):
        column = 0
        for row in matrix:
            column = column | row[j]
        if column == 1: result.append(j)

    return result
    
def sub_set(subbase, base):
    for i in subbase:
        if not i in base: return False
    
    return True

def get_base_of(matrix, subbase):
    if len(subbase) == len(matrix): return subbase
    all_sub_set = get_all_sub_set_with(len(matrix[0]))

    for indexes in [l for l  in all_sub_set if len(l) == len(matrix) and sub_set(subbase, l)]:
        newMatrix = []
        for  row in matrix:
            newMatrix.append([v for i, v in enumerate(row) if i in indexes])
        A = np.array(newMatrix)
        det = np.linalg.det(A)

        if  not det == 0: return indexes 
    return []

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

