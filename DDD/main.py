from adapters.redis_eventpublisher import UUIDEncoder
from socket import create_server
from typing import Text
import uuid
from pydantic.types import UUID1, UUID3

from sanic import Sanic
from sanic import response
from sanic.response import HTTPResponse, json

from domain import commands
from service_layer.unit_of_work import DeliveryUnitOfWork, ShippingUnitOfWork
from storage import shipping_list, delivery_list
from service_layer import messagebus
import views


app = Sanic("My Hello, world app")
id = []
users = []


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


# Chapter 12
@app.route('/list/<user_id>',methods=['GET'])
async def get_list(request,user_id):
    cmd = commands.FreeUser(
        user=user_id
    )
    uow = DeliveryUnitOfWork()
    result = await messagebus.handle(cmd,uow)
    print('user freed.......')
    print(delivery_list)
    return json({'s':'s'})


@app.route('/delivery', methods=['POST'])
async def create_agent(request):
    cmd = commands.AddDelivery(
        name=request.form.get("name") if request.form.get("name") else "adarsha",
        post= "manager",
        permission="all",
    )
    uow = DeliveryUnitOfWork()
    result = await messagebus.handle(cmd,uow)
    print("the ddeliver yylist is ")
    print(delivery_list)
    users.append(delivery_list[0]['user'])
    return json({'delivery agent':'added'})

@app.route('/addtask',methods=['POST'])
async def add_task(request):
    cmd = commands.Allocate(
        user=users[0],
        task=id[0]
    )
    uow = DeliveryUnitOfWork()
    result = await messagebus.handle(cmd,uow)
    print(delivery_list)
    return json({'updated task':'updated_task'})


# cqrs
@app.route('/getshipping', methods=['GET'])
async def get_shipping(request):
    list1 = await views.get_shipping()
    print(shipping_list)
    return json(list1)


@app.route('/getdelivery',methods=['GET'])
async def get_delivery(request):
    list1 = await views.get_delivery()
    print(list1)
    return json(list1)



if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
