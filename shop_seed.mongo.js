// ================================================
// Initialize database
// ================================================
use study_db_shop;

// Clear collections if they already exist
db.customers.drop();
db.products.drop();
db.orders.drop();

// ================================================
// Insert customers
// ================================================
db.customers.insertMany([
    {
        _id: ObjectId("66c100c10000000000000101"),
        name: "Alice Brown",
        email: "alice@example.com",
        address: { city: "Brussels", street: "Main Street 15" }
    },
    {
        _id: ObjectId("66c100c10000000000000102"),
        name: "Bob Martin",
        email: "bob@example.com",
        address: { city: "Antwerp", street: "River Road 7" }
    },
    {
        _id: ObjectId("66c100c10000000000000103"),
        name: "Caroline Smith",
        email: "caroline@example.com",
        address: { city: "Ghent", street: "Forest Avenue 22" }
    },
    {
        _id: ObjectId("66c100c10000000000000104"),
        name: "David Johnson",
        email: "david@example.com",
        address: { city: "Leuven", street: "College 10" }
    },
    {
        _id: ObjectId("66c100c10000000000000105"),
        name: "Eva White",
        email: "eva@example.com",
        address: { city: "Bruges", street: "Old Town 3" }
    }
]);

// ================================================
// Insert products
// ================================================
db.products.insertMany([
    {
        _id: ObjectId("66c200c20000000000000201"),
        name: "Laptop X10",
        price: 1200,
        tags: ["electronics", "laptop"]
    },
    {
        _id: ObjectId("66c200c20000000000000202"),
        name: "Mouse A5",
        price: 25,
        tags: ["electronics", "accessory"]
    },
    {
        _id: ObjectId("66c200c20000000000000203"),
        name: "Office Chair Comfort",
        price: 180,
        tags: ["furniture", "office"]
    },
    {
        _id: ObjectId("66c200c20000000000000204"),
        name: "USB-C Cable 2m",
        price: 12,
        tags: ["electronics", "cable"]
    },
    {
        _id: ObjectId("66c200c20000000000000205"),
        name: "Monitor 27 UltraHD",
        price: 340,
        tags: ["electronics", "monitor"]
    }
]);

// ================================================
// Insert orders
// ================================================
db.orders.insertMany([
    {
        _id: ObjectId("66c300c30000000000000301"),
        customer_id: ObjectId("66c100c10000000000000101"), // Alice
        items: [
            { product_id: ObjectId("66c200c20000000000000201"), qty: 1, price: 1200 },
            { product_id: ObjectId("66c200c20000000000000202"), qty: 2, price: 25 }
        ],
        total: 1250,
        date: ISODate("2024-01-10T10:00:00Z")
    },
    {
        _id: ObjectId("66c300c30000000000000302"),
        customer_id: ObjectId("66c100c10000000000000103"), // Caroline
        items: [
            { product_id: ObjectId("66c200c20000000000000203"), qty: 1, price: 180 },
            { product_id: ObjectId("66c200c20000000000000204"), qty: 3, price: 12 }
        ],
        total: 216,
        date: ISODate("2024-02-05T14:30:00Z")
    },
    {
        _id: ObjectId("66c300c30000000000000303"),
        customer_id: ObjectId("66c100c10000000000000105"), // Eva
        items: [
            { product_id: ObjectId("66c200c20000000000000205"), qty: 1, price: 340 }
        ],
        total: 340,
        date: ISODate("2024-03-01T09:15:00Z")
    },
    {
        _id: ObjectId("66c300c30000000000000304"),
        customer_id: ObjectId("66c100c10000000000000102"), // Bob
        items: [
            { product_id: ObjectId("66c200c20000000000000204"), qty: 4, price: 12 }
        ],
        total: 48,
        date: ISODate("2024-03-11T11:40:00Z")
    }
]);

// ================================================
// Done
// ================================================
print("Database 'study_db_shop' successfully initialized.");
