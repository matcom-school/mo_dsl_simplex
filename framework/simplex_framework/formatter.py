from .prettier_print import prettier, pprint
import numpy as np

class XVar:
    def __getitem__(self, index):
        return Coefficient(index)
    
class Coefficient:
    def __init__(self, index) -> None:
        self.index = index
        self.coefficient = 1
        self.sums = []
        self.rests = []
        self.result = None
        self.simbol = None

    
    def __rmul__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        self.coefficient *= other

        return self
    
    def __mul__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        self.coefficient *= other
        
        return self
    
    def __truediv__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        self.coefficient /= other
    
        return self
    
    def __add__(self, other): 
        if not type(other) == type(self):
            raise TypeError("sum is not defined between different types")
        
        self.sums.append(other)
        return self
    
    def __radd__(self, other): 
        if not type(other) == type(self):
            raise TypeError("sum is not defined between different types")
        
        self.sums.append(other)
        return self

    def __sub__(self, other):
        if not type(other) == type(self):
            raise TypeError("rest is not defined between different types")
        
        self.rests.append(other)
        return self

    def __rsub__(self, other):
        if not type(other) == type(self):
            raise TypeError("rest is not defined between different types")
        
        self.rests.append(other)
        return self
    
    def __lt__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '<'
        return self

        
    def __rlt__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '<'
        return self


    def __le__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '<='
        return self


    def __rle__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '<='
        return self


    def __eq__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '=='
        return self


    def __req__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '=='
        return self


    def __ge__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '>='
        return self


    def __rge__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '>='
        return self


        
    def __gt__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '>'
        return self


        
    def __rgt__(self, other):
        if not type(other) in [type(int()), type(float())]:
            raise TypeError("expect number like coefficient")
        if not self.result is None:
            raise RuntimeError("Innequation don't have more that one comparative")
        
        self.result = other
        self.simbol = '>'
        return self

class Formatter:
    def __init__(self, print) -> None:
        self.ctx = []
        self.Ax = []
        self.b = []
        self.verb = 'min'
        self.__coefficient = None
        self.__matrix = None
        self.print = print

    def __setattr__(self, __name: str, __value) -> None:
        if __name == 'min_z': self.__coefficient = __value
        if __name == 'max_z': 
            self.verb = 'max'
            self.__coefficient = __value
        if __name == 's_a': self.__matrix = __value
        else:
            self.__dict__[__name] = __value
            return 
        if not self.__coefficient is None and not self.__matrix is None:
            self.compose()

    def compose(self):
        cdict = {}
        self.dfs_factors(self.__coefficient, cdict)

        list_dict = []
        keys = list(cdict.keys())
        for row in self.__matrix:
            self.b.append((row.simbol, row.result))
            temp_dict = {}
            self.dfs_factors(row, temp_dict)
            list_dict.append(temp_dict)
            keys += temp_dict.keys()
        
        length = max(keys) + 1
        for _ in range(length):
            self.ctx.append(0)

        for _ in self.b:
            self.Ax.append([0]* length)
        
        for key in cdict.keys():
            self.ctx[key] = cdict[key]
        
        for i, __dict in enumerate(list_dict):
            for key in __dict.keys():
                self.Ax[i][key] = list_dict[i][key]

        
        if self.print: pprint(self)

    def dfs_factors(self, coefficient, _dict):
        _dict[coefficient.index] = coefficient.coefficient
        for sum in coefficient.sums:
            self.dfs_factors(sum, _dict)

        for rest in coefficient.rests:
            rest.coefficient *= -1
            self.dfs_factors(rest, _dict)

GREATER = '>'
GREATER_EQUAL = ">="
LOWER = '<'
LOWER_EQUAL = '<='
EQUAL = '==' 

class LinealOptimizationProblem:
    def __init__(self, verb, ctx, Ax, b) -> None:
        assert verb in ['min', 'max'], 'Unknown verb to LOP'

        for sign, v in b:
           assert sign in [ GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL, EQUAL ], 'Unknown sing to LOP'

        self.ctx = ctx
        self.Ax = Ax
        self.b = b
        self.verb = verb
    
    @property
    def result_vector(self):
        return np.array([v for _, v in self.b])

def format_componet(look=False):
    return XVar(), Formatter(print)
 

def add_column(matrix):
    for row in matrix: 
        row.append(0)

def stand_form_func(row, simbol):
    if simbol in [GREATER, GREATER_EQUAL]: row[-1] = -1
    elif simbol in [LOWER, LOWER_EQUAL]: row[-1] = 1

@prettier
def get_stand_form(pol: LinealOptimizationProblem, func = stand_form_func):
    rctx, rAx, rb = pol.ctx, pol.Ax.copy(), [(EQUAL, val) for s, val in pol.b]

    if pol.verb == 'max': 
        rctx = [min] + [c * -1 for c in rctx]
    
    for i, val in enumerate(pol.b):
        simbol, result = val
        add_column(rAx)
        rctx.append(0)
        func(rAx[i], simbol)

    return LinealOptimizationProblem('min', rctx, rAx, rb)

    