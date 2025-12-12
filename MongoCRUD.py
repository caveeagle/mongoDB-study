
import re
from datetime import datetime, UTC

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

    customers = db.customers
    products = db.products
    orders = db.orders
    
    # --- 0) Snapshot initial document counts per collection
    initial_counts = {
        "customers": customers.count_documents({}),
        "products": products.count_documents({}),
        "orders": orders.count_documents({}),
    }
    #print("Initial counts:", initial_counts)
    
    # --- Scenario parameters
    new_product_name = "Notebook Z999"
    new_product_price = 450
    price_increase_abs = 70  # raise the price by a fixed amount
    customer_name_query = "Alice"  # existing customer; case-insensitive substring search
    
    # Track resources we create
    created_product_id = None
    created_order_id = None
    
    try:
        # --- 1) INSERT: insert a new product with a "similar-name" check
        # Similarity implemented as a case-insensitive substring (regex)
        name_regex = {"$regex": re.escape(new_product_name), "$options": "i"}
        similar_count = products.count_documents({"name": name_regex})
        if similar_count > 0:
            raise RuntimeError(
                f"Found {similar_count} product(s) with a name similar to '{new_product_name}'. Insert canceled."
            )
    
        insert_res = products.insert_one({
            "name": new_product_name,
            "price": new_product_price,
            "tags": ["demo", "example"]
        })
        created_product_id = insert_res.inserted_id

        print(f"Inserted product: {created_product_id} name='{new_product_name}', price={new_product_price}")
    
        # --- 2) UPDATE: increase the product price
        upd_res = products.update_one(
            {"_id": created_product_id},
            {"$inc": {"price": price_increase_abs}}
        )
        assert upd_res.matched_count == 1, "Price update: product not found"
        assert upd_res.modified_count == 1, "Price update: document not modified (increment may be 0)"
        updated_product = products.find_one({"_id": created_product_id}, {"price": 1})
        print(f"Updated product price to: {updated_product['price']}")
    
        # --- 3) CREATE ORDER: find the customer by name (must be exactly one) and create an order for this product
        cust_regex = {"$regex": re.escape(customer_name_query), "$options": "i"}
        matched_customers = list(customers.find({"name": cust_regex}))
        if len(matched_customers) != 1:
            raise RuntimeError(
                f"Expected exactly 1 customer for name ~ '{customer_name_query}', found: {len(matched_customers)}"
            )
        customer = matched_customers[0]
        customer_id = customer["_id"]
    
        # Item price is captured in the order at the time of purchase
        current_price = updated_product["price"]
        qty = 1
        order_doc = {
            "customer_id": customer_id,
            "items": [
                {"product_id": created_product_id, "qty": qty, "price": current_price}
            ],
            "total": qty * current_price,
            "date": datetime.now(UTC)
        }
        order_res = orders.insert_one(order_doc)
        created_order_id = order_res.inserted_id

        print(f"Inserted order: {created_order_id} for customer={customer_id} total={order_doc['total']}")
    
        # --- (Optional) Verify the order exists and is correctly linked
        loaded_order = orders.find_one({"_id": created_order_id})
        assert loaded_order is not None, "Order not found right after insert"
        assert loaded_order["customer_id"] == customer_id, "customer_id mismatch in the order"
        assert loaded_order["items"][0]["product_id"] == created_product_id, "Product in the order does not match"
        
        ####################################################

        # Print only the order we just created (place right after inserting the order)
        order = orders.find_one({"_id": created_order_id}, {"items": 1, "customer_id": 1})
        
        customer = customers.find_one({"_id": order["customer_id"]}, {"name": 1})
        customer_name = customer["name"] if customer else "Unknown customer"
        
        item_strings = []
        for it in order["items"]:
            prod = products.find_one({"_id": it["product_id"]}, {"name": 1})
            prod_name = prod["name"] if prod else "Unknown product"
            item_strings.append(f"{prod_name} x{it['qty']}")
        
        items_text = ", ".join(item_strings)
        
        short_order_id = int.from_bytes(created_order_id.binary[-3:], byteorder="big")

        
        print(f"\nOrder #{short_order_id} for {items_text} by {customer_name}\n")
        
        ####################################################
        
        # --- 4) DELETE: remove all created resources (with checks)
        del_order_res = orders.delete_one({"_id": created_order_id})
        assert del_order_res.deleted_count == 1, "Delete order: document not deleted"
    
        del_product_res = products.delete_one({"_id": created_product_id})
        assert del_product_res.deleted_count == 1, "Delete product: document not deleted"
    
        print("Created order and product were deleted successfully.")
    
        # --- 5) Post-check invariant: collection document counts unchanged
        final_counts = {
            "customers": customers.count_documents({}),
            "products": products.count_documents({}),
            "orders": orders.count_documents({}),
        }
        #print("Final counts:", final_counts)
    
        assert final_counts == initial_counts, (
            f"Document counts mismatch: initial={initial_counts}, final={final_counts}"
        )
        print("Invariant OK: collection document counts are unchanged.")
    
    except Exception as e:
        print(f"ERROR: {e}")
    
        # Best-effort rollback to keep counts unchanged
        if created_order_id is not None:
            orders.delete_one({"_id": created_order_id})
        if created_product_id is not None:
            products.delete_one({"_id": created_product_id})
        raise  # re-raise for visibility
    


    
###############################

print('Job finished!')

###############################
