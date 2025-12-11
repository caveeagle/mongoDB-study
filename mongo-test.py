
from pymongo import MongoClient

import config

SERVER = config.SERVER
USER   = config.USER
PASSWD = config.PASSWD

###############################


REMOTE = 0

if( not REMOTE ):
    SERVER = 'localhost'


client = MongoClient(
    host=SERVER,
    port=27017,
    username=USER,
    password=PASSWD
)

db = client['study_db_shop']

###############################

collections = db.list_collection_names()

if(0):
    print('All collections:\n')
    for n in collections:
        print(n)
    print('\n')

###############################

if(1):

    pipeline = [
        # 1. Соединяем orders с customers по customer_id
        {
            '$lookup': {
                'from': 'customers',
                'localField': 'customer_id',
                'foreignField': '_id',
                'as': 'customer'
            }
        },
        # 2. Оставляем только те заказы, где имя содержит Alice
        {
            '$match': {
                'customer.name': {'$regex': 'Alice', '$options': 'i'}
            }
        },
        # 3. Разворачиваем массив items (одна строка — один товар из заказа)
        { '$unwind': '$items' },
        # 4. Соединяем с products по product_id
        {
            '$lookup': {
                'from': 'products',
                'localField': 'items.product_id',
                'foreignField': '_id',
                'as': 'product'
            }
        },
        # 5. Разворачиваем найденный продукт (всегда 1 элемент)
        { '$unwind': '$product' },
        # 6. Группируем по имени пользователя: список товаров и общая сумма
        {
            '$group': {
                '_id': '$customer.name',
                'products': { '$addToSet': '$product.name' },
                'total': { '$sum': { '$multiply': [ '$items.qty', '$items.price' ] } }
            }
        }
    ]
    
    ##############################################
    
    result = list(db.orders.aggregate(pipeline)) 
    
    if result:
        print("User:", result[0]['_id'][0])
        print("Products:", result[0]['products'])
        print("Total amount:", result[0]['total'])
    else:
        print("Not found")
    
###############################

print('Job finished!')

###############################
