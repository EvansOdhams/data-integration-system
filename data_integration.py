"""
Multi-Source Data Integration System
Python script to integrate data from multiple sources into a centralized database
"""

import sqlite3
import csv
import os
from datetime import datetime, date
from typing import List, Dict, Any

class DataIntegrator:
    """Handles integration of data from multiple sources into the centralized database"""
    
    def __init__(self, db_path: str = 'integration_database.db'):
        """
        Initialize the data integrator
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # Enable foreign key constraints
        self.cursor.execute("PRAGMA foreign_keys = ON")
        print(f"Connected to database: {self.db_path}")
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_schema(self, schema_file: str = 'schema.sql'):
        """
        Create database schema from SQL file
        
        Args:
            schema_file: Path to the SQL schema file
        """
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema creation
        self.cursor.executescript(schema_sql)
        self.conn.commit()
        print(f"Schema created from {schema_file}")
    
    def import_customer_data(self, customer_file: str = 'customer_data.sql'):
        """
        Import customer data from SQL file (simulating data from Customer Data System)
        
        Args:
            customer_file: Path to the SQL file containing customer data
        """
        if not os.path.exists(customer_file):
            raise FileNotFoundError(f"Customer data file not found: {customer_file}")
        
        with open(customer_file, 'r') as f:
            customer_sql = f.read()
        
        # Execute customer data insertion
        self.cursor.executescript(customer_sql)
        self.conn.commit()
        
        # Count imported customers
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        count = self.cursor.fetchone()[0]
        print(f"Imported {count} customers from {customer_file}")
    
    def import_product_data(self, product_file: str = 'product_data.csv'):
        """
        Import product data from CSV file (simulating data from Product Data System)
        
        Args:
            product_file: Path to the CSV file containing product data
        """
        if not os.path.exists(product_file):
            raise FileNotFoundError(f"Product data file not found: {product_file}")
        
        with open(product_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            
            inserted_count = 0
            skipped_count = 0
            
            for row in csv_reader:
                try:
                    # Validate and clean data
                    product_id = int(row['product_id'])
                    product_name = row['product_name'].strip()
                    description = row.get('description', '').strip()
                    price = float(row['price'])
                    stock_quantity = int(row['stock_quantity'])
                    category = row.get('category', '').strip()
                    supplier = row.get('supplier', '').strip()
                    
                    # Data validation
                    if price < 0:
                        print(f"Warning: Invalid price for product {product_id}, skipping")
                        skipped_count += 1
                        continue
                    
                    if stock_quantity < 0:
                        print(f"Warning: Invalid stock quantity for product {product_id}, setting to 0")
                        stock_quantity = 0
                    
                    # Insert product data
                    self.cursor.execute("""
                        INSERT INTO products 
                        (product_id, product_name, description, price, stock_quantity, category, supplier)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (product_id, product_name, description, price, stock_quantity, category, supplier))
                    
                    inserted_count += 1
                    
                except (ValueError, KeyError) as e:
                    print(f"Error processing row: {row}. Error: {e}")
                    skipped_count += 1
                    continue
        
        self.conn.commit()
        print(f"Imported {inserted_count} products from {product_file}")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} invalid product records")
    
    def create_sample_orders(self):
        """
        Create sample order data to link customers and products
        This simulates order transactions after data integration
        """
        # Sample orders data
        orders_data = [
            (1, 1, 101, '2024-01-15', 1, 1299.99),
            (2, 1, 102, '2024-01-15', 2, 29.99),
            (3, 2, 201, '2024-01-20', 1, 299.99),
            (4, 2, 202, '2024-01-20', 1, 39.99),
            (5, 3, 103, '2024-02-01', 1, 89.99),
            (6, 3, 104, '2024-02-01', 1, 399.99),
            (7, 4, 301, '2024-02-10', 3, 34.99),
            (8, 4, 302, '2024-02-10', 2, 19.99),
            (9, 5, 203, '2024-02-15', 1, 599.99),
            (10, 5, 204, '2024-02-15', 1, 79.99),
            (11, 6, 105, '2024-02-20', 4, 49.99),
            (12, 7, 101, '2024-03-01', 1, 1299.99),
            (13, 7, 103, '2024-03-01', 1, 89.99),
            (14, 8, 201, '2024-03-05', 2, 299.99),
            (15, 9, 104, '2024-03-10', 1, 399.99),
            (16, 9, 105, '2024-03-10', 2, 49.99),
            (17, 10, 301, '2024-03-15', 5, 34.99),
            (18, 10, 302, '2024-03-15', 3, 19.99),
            (19, 1, 203, '2024-03-20', 1, 599.99),
            (20, 2, 103, '2024-03-25', 2, 89.99),
        ]
        
        inserted_count = 0
        skipped_count = 0
        
        for order_id, customer_id, product_id, order_date, quantity, unit_price in orders_data:
            try:
                # Validate foreign keys exist
                self.cursor.execute("SELECT customer_id FROM customers WHERE customer_id = ?", (customer_id,))
                if not self.cursor.fetchone():
                    print(f"Warning: Customer {customer_id} not found, skipping order {order_id}")
                    skipped_count += 1
                    continue
                
                self.cursor.execute("SELECT product_id FROM products WHERE product_id = ?", (product_id,))
                if not self.cursor.fetchone():
                    print(f"Warning: Product {product_id} not found, skipping order {order_id}")
                    skipped_count += 1
                    continue
                
                # Insert order
                self.cursor.execute("""
                    INSERT INTO orders 
                    (order_id, customer_id, product_id, order_date, quantity, unit_price, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'completed')
                """, (order_id, customer_id, product_id, order_date, quantity, unit_price))
                
                inserted_count += 1
                
            except Exception as e:
                print(f"Error inserting order {order_id}: {e}")
                skipped_count += 1
                continue
        
        self.conn.commit()
        print(f"Created {inserted_count} sample orders")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} invalid orders")
    
    def validate_data_integrity(self):
        """
        Validate data integrity and consistency
        Returns a report of validation results
        """
        print("\n=== Data Integrity Validation ===")
        
        validation_results = {
            'customers': {'total': 0, 'valid': 0, 'issues': []},
            'products': {'total': 0, 'valid': 0, 'issues': []},
            'orders': {'total': 0, 'valid': 0, 'issues': []},
            'foreign_keys': {'valid': True, 'issues': []}
        }
        
        # Validate customers
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        validation_results['customers']['total'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("""
            SELECT customer_id, email 
            FROM customers 
            WHERE email IS NULL OR email = '' OR first_name IS NULL OR last_name IS NULL
        """)
        invalid_customers = self.cursor.fetchall()
        validation_results['customers']['issues'] = invalid_customers
        validation_results['customers']['valid'] = validation_results['customers']['total'] - len(invalid_customers)
        
        # Validate products
        self.cursor.execute("SELECT COUNT(*) FROM products")
        validation_results['products']['total'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("""
            SELECT product_id, product_name 
            FROM products 
            WHERE product_name IS NULL OR product_name = '' OR price IS NULL OR price < 0
        """)
        invalid_products = self.cursor.fetchall()
        validation_results['products']['issues'] = invalid_products
        validation_results['products']['valid'] = validation_results['products']['total'] - len(invalid_products)
        
        # Validate orders
        self.cursor.execute("SELECT COUNT(*) FROM orders")
        validation_results['orders']['total'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("""
            SELECT order_id 
            FROM orders 
            WHERE quantity IS NULL OR quantity <= 0 OR unit_price IS NULL OR unit_price < 0
        """)
        invalid_orders = self.cursor.fetchall()
        validation_results['orders']['issues'] = invalid_orders
        validation_results['orders']['valid'] = validation_results['orders']['total'] - len(invalid_orders)
        
        # Validate foreign keys
        self.cursor.execute("""
            SELECT o.order_id, o.customer_id, o.product_id
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            LEFT JOIN products p ON o.product_id = p.product_id
            WHERE c.customer_id IS NULL OR p.product_id IS NULL
        """)
        orphaned_orders = self.cursor.fetchall()
        validation_results['foreign_keys']['issues'] = orphaned_orders
        validation_results['foreign_keys']['valid'] = len(orphaned_orders) == 0
        
        # Print validation report
        print(f"Customers: {validation_results['customers']['valid']}/{validation_results['customers']['total']} valid")
        if validation_results['customers']['issues']:
            print(f"  Issues: {validation_results['customers']['issues']}")
        
        print(f"Products: {validation_results['products']['valid']}/{validation_results['products']['total']} valid")
        if validation_results['products']['issues']:
            print(f"  Issues: {validation_results['products']['issues']}")
        
        print(f"Orders: {validation_results['orders']['valid']}/{validation_results['orders']['total']} valid")
        if validation_results['orders']['issues']:
            print(f"  Issues: {validation_results['orders']['issues']}")
        
        print(f"Foreign Keys: {'Valid' if validation_results['foreign_keys']['valid'] else 'Invalid'}")
        if validation_results['foreign_keys']['issues']:
            print(f"  Orphaned orders: {validation_results['foreign_keys']['issues']}")
        
        return validation_results
    
    def run_integration(self):
        """Run the complete data integration process"""
        print("=" * 60)
        print("Multi-Source Data Integration System")
        print("=" * 60)
        
        try:
            # Connect to database
            self.connect()
            
            # Create schema
            print("\n[Step 1] Creating database schema...")
            self.create_schema()
            
            # Import customer data
            print("\n[Step 2] Importing customer data from Customer Data System...")
            self.import_customer_data()
            
            # Import product data
            print("\n[Step 3] Importing product data from Product Data System (CSV)...")
            self.import_product_data()
            
            # Create sample orders
            print("\n[Step 4] Creating sample order data...")
            self.create_sample_orders()
            
            # Validate data integrity
            print("\n[Step 5] Validating data integrity...")
            validation_results = self.validate_data_integrity()
            
            print("\n" + "=" * 60)
            print("Data integration completed successfully!")
            print("=" * 60)
            
            return validation_results
            
        except Exception as e:
            print(f"\nError during integration: {e}")
            raise
        finally:
            self.close()


if __name__ == "__main__":
    integrator = DataIntegrator()
    integrator.run_integration()

