"""
Multi-Source Data Integration System - Supabase Version
Python script to integrate data from multiple sources into Supabase (PostgreSQL)
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

class SupabaseIntegrator:
    """Handles integration of data from multiple sources into Supabase"""
    
    def __init__(self):
        """Initialize the Supabase integrator"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.db_url = os.getenv('DATABASE_URL')  # Direct PostgreSQL connection
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.conn = None
        self.cursor = None
        
    def connect_db(self):
        """Establish direct PostgreSQL connection for schema operations"""
        if self.db_url:
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor()
            print("Connected to Supabase PostgreSQL database")
        else:
            print("Warning: DATABASE_URL not set. Schema operations will be limited.")
    
    def close_db(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_schema(self, schema_file: str = 'schema_supabase.sql'):
        """
        Create database schema from SQL file
        
        Args:
            schema_file: Path to the SQL schema file
        """
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        if not self.db_url:
            raise ValueError("DATABASE_URL required for schema creation. Use Supabase SQL Editor instead.")
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema creation
        self.cursor.execute(schema_sql)
        self.conn.commit()
        print(f"Schema created from {schema_file}")
    
    def import_customer_data(self, customer_file: str = 'customer_data.sql'):
        """
        Import customer data from SQL file using Supabase client
        
        Args:
            customer_file: Path to the SQL file containing customer data
        """
        if not os.path.exists(customer_file):
            raise FileNotFoundError(f"Customer data file not found: {customer_file}")
        
        with open(customer_file, 'r') as f:
            content = f.read()
        
        # Parse INSERT statements
        customers = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('INSERT INTO') or line.startswith('VALUES'):
                # Extract values from INSERT statement
                if 'VALUES' in line:
                    # Parse VALUES clause
                    values_str = line.split('VALUES')[1].strip().rstrip(';')
                    # Remove parentheses and split
                    values_str = values_str.strip('()')
                    values = [v.strip().strip("'") for v in values_str.split(',')]
                    
                    if len(values) >= 10:
                        customer = {
                            'customer_id': int(values[0]),
                            'first_name': values[1],
                            'last_name': values[2],
                            'email': values[3],
                            'phone': values[4] if values[4] != 'NULL' else None,
                            'address': values[5] if values[5] != 'NULL' else None,
                            'city': values[6] if values[6] != 'NULL' else None,
                            'state': values[7] if values[7] != 'NULL' else None,
                            'zip_code': values[8] if values[8] != 'NULL' else None,
                            'country': values[9] if len(values) > 9 and values[9] != 'NULL' else 'USA'
                        }
                        customers.append(customer)
        
        # Insert using Supabase
        if customers:
            # Use upsert to handle existing records
            result = self.supabase.table('customers').upsert(customers).execute()
            print(f"Imported {len(customers)} customers")
        else:
            print("No customer data found to import")
    
    def import_customer_data_csv(self, customer_file: str = None):
        """Import customer data from CSV file"""
        if customer_file and os.path.exists(customer_file):
            customers = []
            with open(customer_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    customer = {
                        'customer_id': int(row['customer_id']),
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'email': row['email'],
                        'phone': row.get('phone'),
                        'address': row.get('address'),
                        'city': row.get('city'),
                        'state': row.get('state'),
                        'zip_code': row.get('zip_code'),
                        'country': row.get('country', 'USA')
                    }
                    customers.append(customer)
            
            if customers:
                result = self.supabase.table('customers').upsert(customers).execute()
                print(f"Imported {len(customers)} customers from CSV")
    
    def import_product_data(self, product_file: str = 'product_data.csv'):
        """
        Import product data from CSV file
        
        Args:
            product_file: Path to the CSV file containing product data
        """
        if not os.path.exists(product_file):
            raise FileNotFoundError(f"Product data file not found: {product_file}")
        
        products = []
        with open(product_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            
            for row in csv_reader:
                try:
                    product = {
                        'product_id': int(row['product_id']),
                        'product_name': row['product_name'].strip(),
                        'description': row.get('description', '').strip(),
                        'price': float(row['price']),
                        'stock_quantity': int(row['stock_quantity']),
                        'category': row.get('category', '').strip(),
                        'supplier': row.get('supplier', '').strip()
                    }
                    
                    # Validation
                    if product['price'] < 0:
                        print(f"Warning: Invalid price for product {product['product_id']}, skipping")
                        continue
                    
                    if product['stock_quantity'] < 0:
                        product['stock_quantity'] = 0
                    
                    products.append(product)
                    
                except (ValueError, KeyError) as e:
                    print(f"Error processing row: {row}. Error: {e}")
                    continue
        
        if products:
            result = self.supabase.table('products').upsert(products).execute()
            print(f"Imported {len(products)} products from {product_file}")
    
    def create_sample_orders(self):
        """Create sample order data to link customers and products"""
        orders_data = [
            {'order_id': 1, 'customer_id': 1, 'product_id': 101, 'order_date': '2024-01-15', 'quantity': 1, 'unit_price': 1299.99, 'status': 'completed'},
            {'order_id': 2, 'customer_id': 1, 'product_id': 102, 'order_date': '2024-01-15', 'quantity': 2, 'unit_price': 29.99, 'status': 'completed'},
            {'order_id': 3, 'customer_id': 2, 'product_id': 201, 'order_date': '2024-01-20', 'quantity': 1, 'unit_price': 299.99, 'status': 'completed'},
            {'order_id': 4, 'customer_id': 2, 'product_id': 202, 'order_date': '2024-01-20', 'quantity': 1, 'unit_price': 39.99, 'status': 'completed'},
            {'order_id': 5, 'customer_id': 3, 'product_id': 103, 'order_date': '2024-02-01', 'quantity': 1, 'unit_price': 89.99, 'status': 'completed'},
            {'order_id': 6, 'customer_id': 3, 'product_id': 104, 'order_date': '2024-02-01', 'quantity': 1, 'unit_price': 399.99, 'status': 'completed'},
            {'order_id': 7, 'customer_id': 4, 'product_id': 301, 'order_date': '2024-02-10', 'quantity': 3, 'unit_price': 34.99, 'status': 'completed'},
            {'order_id': 8, 'customer_id': 4, 'product_id': 302, 'order_date': '2024-02-10', 'quantity': 2, 'unit_price': 19.99, 'status': 'completed'},
            {'order_id': 9, 'customer_id': 5, 'product_id': 203, 'order_date': '2024-02-15', 'quantity': 1, 'unit_price': 599.99, 'status': 'completed'},
            {'order_id': 10, 'customer_id': 5, 'product_id': 204, 'order_date': '2024-02-15', 'quantity': 1, 'unit_price': 79.99, 'status': 'completed'},
            {'order_id': 11, 'customer_id': 6, 'product_id': 105, 'order_date': '2024-02-20', 'quantity': 4, 'unit_price': 49.99, 'status': 'completed'},
            {'order_id': 12, 'customer_id': 7, 'product_id': 101, 'order_date': '2024-03-01', 'quantity': 1, 'unit_price': 1299.99, 'status': 'completed'},
            {'order_id': 13, 'customer_id': 7, 'product_id': 103, 'order_date': '2024-03-01', 'quantity': 1, 'unit_price': 89.99, 'status': 'completed'},
            {'order_id': 14, 'customer_id': 8, 'product_id': 201, 'order_date': '2024-03-05', 'quantity': 2, 'unit_price': 299.99, 'status': 'completed'},
            {'order_id': 15, 'customer_id': 9, 'product_id': 104, 'order_date': '2024-03-10', 'quantity': 1, 'unit_price': 399.99, 'status': 'completed'},
            {'order_id': 16, 'customer_id': 9, 'product_id': 105, 'order_date': '2024-03-10', 'quantity': 2, 'unit_price': 49.99, 'status': 'completed'},
            {'order_id': 17, 'customer_id': 10, 'product_id': 301, 'order_date': '2024-03-15', 'quantity': 5, 'unit_price': 34.99, 'status': 'completed'},
            {'order_id': 18, 'customer_id': 10, 'product_id': 302, 'order_date': '2024-03-15', 'quantity': 3, 'unit_price': 19.99, 'status': 'completed'},
            {'order_id': 19, 'customer_id': 1, 'product_id': 203, 'order_date': '2024-03-20', 'quantity': 1, 'unit_price': 599.99, 'status': 'completed'},
            {'order_id': 20, 'customer_id': 2, 'product_id': 103, 'order_date': '2024-03-25', 'quantity': 2, 'unit_price': 89.99, 'status': 'completed'},
        ]
        
        inserted_count = 0
        skipped_count = 0
        
        for order in orders_data:
            try:
                # Validate foreign keys exist
                customer_check = self.supabase.table('customers').select('customer_id').eq('customer_id', order['customer_id']).execute()
                if not customer_check.data:
                    print(f"Warning: Customer {order['customer_id']} not found, skipping order {order['order_id']}")
                    skipped_count += 1
                    continue
                
                product_check = self.supabase.table('products').select('product_id').eq('product_id', order['product_id']).execute()
                if not product_check.data:
                    print(f"Warning: Product {order['product_id']} not found, skipping order {order['order_id']}")
                    skipped_count += 1
                    continue
                
                # Insert order
                result = self.supabase.table('orders').upsert(order).execute()
                inserted_count += 1
                
            except Exception as e:
                print(f"Error inserting order {order['order_id']}: {e}")
                skipped_count += 1
                continue
        
        print(f"Created {inserted_count} sample orders")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} invalid orders")
    
    def validate_data_integrity(self):
        """Validate data integrity and consistency"""
        print("\n=== Data Integrity Validation ===")
        
        # Get counts
        customers_result = self.supabase.table('customers').select('customer_id', count='exact').execute()
        products_result = self.supabase.table('products').select('product_id', count='exact').execute()
        orders_result = self.supabase.table('orders').select('order_id', count='exact').execute()
        
        customer_count = customers_result.count if hasattr(customers_result, 'count') else len(customers_result.data)
        product_count = products_result.count if hasattr(products_result, 'count') else len(products_result.data)
        order_count = orders_result.count if hasattr(orders_result, 'count') else len(orders_result.data)
        
        print(f"Customers: {customer_count}")
        print(f"Products: {product_count}")
        print(f"Orders: {order_count}")
        
        return {
            'customers': customer_count,
            'products': product_count,
            'orders': order_count
        }
    
    def run_integration(self):
        """Run the complete data integration process"""
        print("=" * 60)
        print("Multi-Source Data Integration System - Supabase")
        print("=" * 60)
        
        try:
            # Import customer data
            print("\n[Step 1] Importing customer data from Customer Data System...")
            self.import_customer_data()
            
            # Import product data
            print("\n[Step 2] Importing product data from Product Data System (CSV)...")
            self.import_product_data()
            
            # Create sample orders
            print("\n[Step 3] Creating sample order data...")
            self.create_sample_orders()
            
            # Validate data integrity
            print("\n[Step 4] Validating data integrity...")
            validation_results = self.validate_data_integrity()
            
            print("\n" + "=" * 60)
            print("Data integration completed successfully!")
            print("=" * 60)
            
            return validation_results
            
        except Exception as e:
            print(f"\nError during integration: {e}")
            raise


if __name__ == "__main__":
    integrator = SupabaseIntegrator()
    integrator.run_integration()

