def prettier(fn):
    def  f( *arg, **kw):
        try:
            look = kw['look']
            kw.pop('look')
        except KeyError: look = False 
        result = fn(*arg, **kw)
        if look: pprint(result)
        return result
    return f

def pprint(pol):
    result = f'{pol.verb} z = '

    str_coef = lambda x : f'+ {x}' if x >= 0 else f'- {abs(x)}'

    for i, coef in enumerate(pol.ctx):
        if i == 0: result += f'{coef} x{0} '
        elif coef == 0: continue
        else: result += f'{str_coef(coef)} x{i} '
    
    result += '\n'

    for i, row in enumerate(pol.Ax):
        result += "        "
        for j, value in enumerate(row):
            if j == 0: result += f'{value} x{0} '
            elif value == 0: continue
            else: result += f'{str_coef(value)} x{j} '

        result += f' {pol.b[i][0]} {pol.b[i][1]}\n'

    print(result)

def print_number(n):
    if n == 0: return '  0.0000'
    elif n < 0: return ' %02.4f'%n
    else: return '  %02.4f'%n