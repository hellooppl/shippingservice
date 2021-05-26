from typing import List
from storage import delivery_list,shipping_list
from copy import deepcopy

def copy():
    for i in shipping_list:
        i = i.copy()
    shipping_copy = list(shipping_list)
    for j in delivery_list:
        j = j.copy()
    delivery_copy = list(delivery_list)
    return shipping_copy,delivery_copy

def structure_code(Li,par):
    for i in Li:
        del i[par]
    return Li

async def get_shipping(id=None):
    shipping_copy =copy()[0]
    if not id:
        return structure_code(shipping_copy,'_id')
    else:
        for i in shipping_copy:
            if i['_id']==id:
                return structure_code(i,'_id')

async def get_delivery(id=None):
    delivery_copy = copy()[1]
    if not id:
        return structure_code(delivery_copy,'user')
    for i in delivery_list:
        if i['user']==id:
            return structure_code(delivery_copy,'user')