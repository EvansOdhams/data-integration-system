"""
Sample data used as fallbacks when Supabase is not connected.
This ensures the Streamlit UI remains functional for demonstrations.
"""

from typing import List, Dict


SAMPLE_CUSTOMERS: List[Dict] = [
    {"customer_id": 1, "first_name": "John", "last_name": "Smith", "email": "john.smith@email.com",
     "phone": "555-0101", "address": "123 Main Street", "city": "New York", "state": "NY",
     "zip_code": "10001", "country": "USA"},
    {"customer_id": 2, "first_name": "Emily", "last_name": "Johnson", "email": "emily.johnson@email.com",
     "phone": "555-0102", "address": "456 Oak Avenue", "city": "Los Angeles", "state": "CA",
     "zip_code": "90001", "country": "USA"},
    {"customer_id": 3, "first_name": "Michael", "last_name": "Williams", "email": "michael.williams@email.com",
     "phone": "555-0103", "address": "789 Pine Road", "city": "Chicago", "state": "IL",
     "zip_code": "60601", "country": "USA"},
    {"customer_id": 4, "first_name": "Sarah", "last_name": "Brown", "email": "sarah.brown@email.com",
     "phone": "555-0104", "address": "321 Elm Street", "city": "Houston", "state": "TX",
     "zip_code": "77001", "country": "USA"},
    {"customer_id": 5, "first_name": "David", "last_name": "Jones", "email": "david.jones@email.com",
     "phone": "555-0105", "address": "654 Maple Drive", "city": "Phoenix", "state": "AZ",
     "zip_code": "85001", "country": "USA"},
    {"customer_id": 6, "first_name": "Jessica", "last_name": "Garcia", "email": "jessica.garcia@email.com",
     "phone": "555-0106", "address": "987 Cedar Lane", "city": "Philadelphia", "state": "PA",
     "zip_code": "19101", "country": "USA"},
    {"customer_id": 7, "first_name": "Robert", "last_name": "Miller", "email": "robert.miller@email.com",
     "phone": "555-0107", "address": "147 Birch Boulevard", "city": "San Antonio", "state": "TX",
     "zip_code": "78201", "country": "USA"},
    {"customer_id": 8, "first_name": "Amanda", "last_name": "Davis", "email": "amanda.davis@email.com",
     "phone": "555-0108", "address": "258 Spruce Court", "city": "San Diego", "state": "CA",
     "zip_code": "92101", "country": "USA"},
    {"customer_id": 9, "first_name": "James", "last_name": "Rodriguez", "email": "james.rodriguez@email.com",
     "phone": "555-0109", "address": "369 Willow Way", "city": "Dallas", "state": "TX",
     "zip_code": "75201", "country": "USA"},
    {"customer_id": 10, "first_name": "Lisa", "last_name": "Martinez", "email": "lisa.martinez@email.com",
     "phone": "555-0110", "address": "741 Ash Street", "city": "San Jose", "state": "CA",
     "zip_code": "95101", "country": "USA"},
]


SAMPLE_PRODUCTS: List[Dict] = [
    {"product_id": 101, "product_name": "Laptop Pro 15", "description": "High-performance laptop with 16GB RAM and 512GB SSD",
     "price": 1299.99, "stock_quantity": 25, "category": "Electronics", "supplier": "TechCorp Inc."},
    {"product_id": 102, "product_name": "Wireless Mouse", "description": "Ergonomic wireless mouse with Bluetooth connectivity",
     "price": 29.99, "stock_quantity": 150, "category": "Electronics", "supplier": "TechCorp Inc."},
    {"product_id": 103, "product_name": "Mechanical Keyboard", "description": "RGB mechanical keyboard with Cherry MX switches",
     "price": 89.99, "stock_quantity": 75, "category": "Electronics", "supplier": "TechCorp Inc."},
    {"product_id": 104, "product_name": "Monitor 27\"", "description": "4K UHD 27-inch monitor with HDR support",
     "price": 399.99, "stock_quantity": 40, "category": "Electronics", "supplier": "DisplayTech Ltd."},
    {"product_id": 105, "product_name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader",
     "price": 49.99, "stock_quantity": 200, "category": "Electronics", "supplier": "TechCorp Inc."},
    {"product_id": 201, "product_name": "Office Chair", "description": "Ergonomic office chair with lumbar support",
     "price": 299.99, "stock_quantity": 30, "category": "Furniture", "supplier": "ComfortSeating Co."},
    {"product_id": 202, "product_name": "Desk Lamp", "description": "LED desk lamp with adjustable brightness",
     "price": 39.99, "stock_quantity": 100, "category": "Furniture", "supplier": "LightWorks Inc."},
    {"product_id": 203, "product_name": "Standing Desk", "description": "Adjustable height standing desk 48x24 inches",
     "price": 599.99, "stock_quantity": 15, "category": "Furniture", "supplier": "ComfortSeating Co."},
    {"product_id": 204, "product_name": "Monitor Stand", "description": "Aluminum monitor stand with cable management",
     "price": 79.99, "stock_quantity": 60, "category": "Furniture", "supplier": "ComfortSeating Co."},
    {"product_id": 205, "product_name": "Desk Organizer", "description": "Multi-compartment desk organizer",
     "price": 24.99, "stock_quantity": 120, "category": "Furniture", "supplier": "ComfortSeating Co."},
    {"product_id": 301, "product_name": "Notebook Set", "description": "Set of 3 premium notebooks with leather cover",
     "price": 34.99, "stock_quantity": 80, "category": "Stationery", "supplier": "WriteWell Supplies"},
    {"product_id": 302, "product_name": "Pen Set", "description": "Set of 5 premium ballpoint pens",
     "price": 19.99, "stock_quantity": 200, "category": "Stationery", "supplier": "WriteWell Supplies"},
    {"product_id": 303, "product_name": "Desk Calendar", "description": "2024 desk calendar with monthly views",
     "price": 12.99, "stock_quantity": 150, "category": "Stationery", "supplier": "WriteWell Supplies"},
    {"product_id": 304, "product_name": "Sticky Notes", "description": "Assorted color sticky notes pack of 10",
     "price": 8.99, "stock_quantity": 300, "category": "Stationery", "supplier": "WriteWell Supplies"},
    {"product_id": 305, "product_name": "File Folders", "description": "Set of 20 letter-size file folders",
     "price": 15.99, "stock_quantity": 250, "category": "Stationery", "supplier": "WriteWell Supplies"},
]


SAMPLE_ORDERS: List[Dict] = [
    {"order_id": 1, "customer_id": 1, "product_id": 101, "order_date": "2024-01-15", "quantity": 1, "unit_price": 1299.99, "total_amount": 1299.99, "status": "completed"},
    {"order_id": 2, "customer_id": 1, "product_id": 102, "order_date": "2024-01-15", "quantity": 2, "unit_price": 29.99, "total_amount": 59.98, "status": "completed"},
    {"order_id": 3, "customer_id": 2, "product_id": 201, "order_date": "2024-01-20", "quantity": 1, "unit_price": 299.99, "total_amount": 299.99, "status": "completed"},
    {"order_id": 4, "customer_id": 2, "product_id": 202, "order_date": "2024-01-20", "quantity": 1, "unit_price": 39.99, "total_amount": 39.99, "status": "completed"},
    {"order_id": 5, "customer_id": 3, "product_id": 103, "order_date": "2024-02-01", "quantity": 1, "unit_price": 89.99, "total_amount": 89.99, "status": "completed"},
    {"order_id": 6, "customer_id": 3, "product_id": 104, "order_date": "2024-02-01", "quantity": 1, "unit_price": 399.99, "total_amount": 399.99, "status": "completed"},
    {"order_id": 7, "customer_id": 4, "product_id": 301, "order_date": "2024-02-10", "quantity": 3, "unit_price": 34.99, "total_amount": 104.97, "status": "completed"},
    {"order_id": 8, "customer_id": 4, "product_id": 302, "order_date": "2024-02-10", "quantity": 2, "unit_price": 19.99, "total_amount": 39.98, "status": "completed"},
    {"order_id": 9, "customer_id": 5, "product_id": 203, "order_date": "2024-02-15", "quantity": 1, "unit_price": 599.99, "total_amount": 599.99, "status": "completed"},
    {"order_id": 10, "customer_id": 5, "product_id": 204, "order_date": "2024-02-15", "quantity": 1, "unit_price": 79.99, "total_amount": 79.99, "status": "completed"},
    {"order_id": 11, "customer_id": 6, "product_id": 105, "order_date": "2024-02-20", "quantity": 4, "unit_price": 49.99, "total_amount": 199.96, "status": "completed"},
    {"order_id": 12, "customer_id": 7, "product_id": 101, "order_date": "2024-03-01", "quantity": 1, "unit_price": 1299.99, "total_amount": 1299.99, "status": "completed"},
    {"order_id": 13, "customer_id": 7, "product_id": 103, "order_date": "2024-03-01", "quantity": 1, "unit_price": 89.99, "total_amount": 89.99, "status": "completed"},
    {"order_id": 14, "customer_id": 8, "product_id": 201, "order_date": "2024-03-05", "quantity": 2, "unit_price": 299.99, "total_amount": 599.98, "status": "completed"},
    {"order_id": 15, "customer_id": 9, "product_id": 104, "order_date": "2024-03-10", "quantity": 1, "unit_price": 399.99, "total_amount": 399.99, "status": "completed"},
    {"order_id": 16, "customer_id": 9, "product_id": 105, "order_date": "2024-03-10", "quantity": 2, "unit_price": 49.99, "total_amount": 99.98, "status": "completed"},
    {"order_id": 17, "customer_id": 10, "product_id": 301, "order_date": "2024-03-15", "quantity": 5, "unit_price": 34.99, "total_amount": 174.95, "status": "completed"},
    {"order_id": 18, "customer_id": 10, "product_id": 302, "order_date": "2024-03-15", "quantity": 3, "unit_price": 19.99, "total_amount": 59.97, "status": "completed"},
    {"order_id": 19, "customer_id": 1, "product_id": 203, "order_date": "2024-03-20", "quantity": 1, "unit_price": 599.99, "total_amount": 599.99, "status": "completed"},
    {"order_id": 20, "customer_id": 2, "product_id": 103, "order_date": "2024-03-25", "quantity": 2, "unit_price": 89.99, "total_amount": 179.98, "status": "completed"},
]


