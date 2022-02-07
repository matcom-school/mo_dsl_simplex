from operator import index
import numpy as np
from scipy.linalg import lu



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
def get_base_of(matrix):
    all_sub_set = get_all_sub_set_with(len(matrix[0]))

    for indexes in [l for l  in all_sub_set if len(l) == len(matrix)]:
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
    
    return xb, xr, np.array(B), np.array(R)
