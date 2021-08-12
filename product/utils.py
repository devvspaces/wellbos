import random, string
import inflect
p = inflect.engine()

def random_text(p=5):
    return ''.join(random.sample(string.ascii_uppercase + string.digits,p))

def unique_product_code(instance, code=None, length=5):
    if not code:
        code=random_text(length)
        code = f'WB-{code}'
    
    exists = instance.__class__.objects.filter(code = code).exists()
    
    if exists:
        return unique_product_code(instance)
    
    return code

def humanize(val):
    if val:
        return p.ordinal(val)
    return '0'


# def pluralize(val):
#     return p.plural_adj(val)