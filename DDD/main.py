from typing import Text
import uuid

from sanic import Sanic
from sanic.response import HTTPResponse, json

from domain import commands
from service_layer import unit_of_work, messagebus, abstract
from service_layer.unit_of_work import ShippingUnitOfWork
from storage import shipping_list

app = Sanic("My Hello, world app")
id = []


@app.route('/', methods=['POST', 'GET'])
async def add_shipping(request):
    if request.method == 'GET':
        return HTTPResponse('''Welcome to Addy's sanic profile''')
    else:
        cmd = commands.AddShipping(
            category="ss",
            cost=150,
            regionId=1,
            orderId=8,
            insurance=150,
            date_to_ship="2018",
        )
        uow = ShippingUnitOfWork()
        await messagebus.handle(cmd, uow)
        print("the added list is")
        print(shipping_list)
        id.append(shipping_list[0]['_id'])
        return json({'post': 'shipping_list'})


@app.route('/get')
async def get_shipping(request):
    cmd = commands.GetShipping(id_=id[0])
    uow = ShippingUnitOfWork()
    result = await messagebus.handle(cmd, uow)
    return json(result)


@app.route('/update', methods=['POST'])
async def update_shipping(request):
    cmd = commands.Update_date_to_ship(
        shipping=
        date_to_ship='2019'
    )
    uow = ShippingUnitOfWork()
    before = shipping_list
    await messagebus.handle(cmd, uow)
    print('The updated list is ')
    print(shipping_list)
    bo = shipping_list.__hash__() == before.__hash__()
    return json({'updated': bo})


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
