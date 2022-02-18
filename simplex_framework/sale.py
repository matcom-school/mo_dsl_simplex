sale_list = []

with open('sale.txt') as file:
    _text = file.read()
    sale_list = _text.split(',')

def check_sale(f):
    if not f.__name__ in sale_list and not 'all' in sale_list:
        raise AttributeError(f'You have not purchased {f.__name__} function') 

    return f