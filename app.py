import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores


app = Flask(__name__)

@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())} # Return a dictionary


@app.post('/store')
def create_store():
    store_data = request.get_json()
    if 'name' not in store_data:
        abort(400, message='Bad request. Ensure name is provided.')
    else:
        for store in stores.values():
            if store['name'] == store_data['name']:
                abort(400, message='Store already exists.')

    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id}
    stores[store_id]= store
    return store, 201


@app.post('/item')
def create_item():
    item_data = request.get_json()
    if 'store_id' not in item_data or 'price' not in item_data or 'name' not in item_data:
        abort(400, message='Bad request. ensure store_id, price and name are provided.')

    elif item_data['store_id'] not in stores:
        abort(404, message='Store not found.')

    else:
        for item in items.values():
            if item['name'] == item_data['name'] and item['store_id'] == item_data['store_id']:
                abort(400, message='Item already exists.')

    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item

    return item, 201


@app.get('/item')
def get_items():
    return {'items': list(items.values())}


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
       return stores[store_id]
    except KeyError:
        abort(404, message='Store not found.')



@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message='Item not found.')