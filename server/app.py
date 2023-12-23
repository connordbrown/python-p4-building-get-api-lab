#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        baked_goods = []
        for good in BakedGood.query.filter(BakedGood.bakery_id == bakery.id):
            baked_goods_dict = {
                'bakery_id': good.bakery_id,
                'created_at': good.created_at,
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'updated_at': good.updated_at
            }
            baked_goods.append(baked_goods_dict)
        bakery_dict = {
            'baked_goods': baked_goods,
            'created_at': bakery.created_at,
            'id': bakery.id,
            'name': bakery.name,
            'updated_at': bakery.updated_at
        }
        bakeries.append(bakery_dict)

    if bakeries:   
        body = bakeries 
        status = 200
    else:
        body = {'message': f'Bakeries not found.'}
        status = 404
    
    return make_response(body, status)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    if bakery:
        baked_goods = []
        for good in BakedGood.query.filter(BakedGood.bakery_id == id).all():
            baked_goods_dict = {
                'bakery_id': good.bakery_id,
                'created_at': good.created_at,
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'updated_at': good.updated_at
            }
            baked_goods.append(baked_goods_dict)

        body = {
            'baked_goods': baked_goods,
            'created_at': bakery.created_at,
            'id': bakery.id,
            'name': bakery.name,
            'updated_at': bakery.updated_at
        }
        status = 200
    else:
        body = {'message': f'Bakery {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_goods = []
    # use attribute
    for good in BakedGood.query.order_by(BakedGood.price.desc()).all():
        if bakery := Bakery.query.filter(Bakery.id == good.bakery_id).first():
            baked_good_dict = {
                'bakery': {
                    'created_at': bakery.created_at,
                    'id': bakery.id,
                    'name': bakery.name,
                    'updated_at': bakery.updated_at
                },
                'bakery_id': good.bakery_id,
                'created_at': good.created_at,
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'updated_at': good.updated_at
            }
            sorted_goods.append(baked_good_dict)
    
    if sorted_goods:
        body = sorted_goods
        status = 200
    else:
        body = {'message': f'Goods not found.'}
        status = 404
    
    return make_response(body, status)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good_dict = {}
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bakery := Bakery.query.filter(Bakery.id == good.bakery_id).first():
        baked_good_dict = {
            'bakery': {
                'created_at': bakery.created_at,
                'id': bakery.id,
                'name': bakery.name,
                'updated_at': bakery.updated_at
            },
            'bakery_id': good.bakery_id,
            'created_at': good.created_at,
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'updated_at': good.updated_at
        }

    if good:
        body = baked_good_dict
        status = 200
    else:
        body = {'message': f'Good not found.'}
        status = 404

    return make_response(body, status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
