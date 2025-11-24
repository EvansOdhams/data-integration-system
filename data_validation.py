"""
Data Validation Module
Ensures data consistency and integrity during and after integration
"""

import sqlite3
from typing import Dict, List, Tuple

class DataValidator:
    """Validates data consistency and integrity"""
    
    def __init__(self, db_path: str = 'integration_database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def validate_customers(self) -> Dict:
        """Validate customer data"""
        issues = []
        
        # Check for NULL required fields
        self.cursor.execute("""
            SELECT customer_id, first_name, last_name, email
            FROM customers
            WHERE first_name IS NULL OR last_name IS NULL OR email IS NULL
        """)
        null_fields = self.cursor.fetchall()
        if null_fields:
            issues.append(f"Customers with NULL required fields: {null_fields}")
        
        # Check for duplicate emails
        self.cursor.execute("""
            SELECT email, COUNT(*) as count
            FROM customers
            GROUP BY email
            HAVING count > 1
        """)
        duplicate_emails = self.cursor.fetchall()
        if duplicate_emails:
            issues.append(f"Duplicate email addresses: {duplicate_emails}")
        
        # Check for invalid email format (basic check)
        self.cursor.execute("""
            SELECT customer_id, email
            FROM customers
            WHERE email NOT LIKE '%@%.%'
        """)
        invalid_emails = self.cursor.fetchall()
        if invalid_emails:
            issues.append(f"Invalid email format: {invalid_emails}")
        
        return {
            'table': 'customers',
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def validate_products(self) -> Dict:
        """Validate product data"""
        issues = []
        
        # Check for NULL required fields
        self.cursor.execute("""
            SELECT product_id, product_name, price
            FROM products
            WHERE product_name IS NULL OR price IS NULL
        """)
        null_fields = self.cursor.fetchall()
        if null_fields:
            issues.append(f"Products with NULL required fields: {null_fields}")
        
        # Check for negative prices
        self.cursor.execute("""
            SELECT product_id, product_name, price
            FROM products
            WHERE price < 0
        """)
        negative_prices = self.cursor.fetchall()
        if negative_prices:
            issues.append(f"Products with negative prices: {negative_prices}")
        
        # Check for negative stock quantities
        self.cursor.execute("""
            SELECT product_id, product_name, stock_quantity
            FROM products
            WHERE stock_quantity < 0
        """)
        negative_stock = self.cursor.fetchall()
        if negative_stock:
            issues.append(f"Products with negative stock: {negative_stock}")
        
        # Check for duplicate product IDs
        self.cursor.execute("""
            SELECT product_id, COUNT(*) as count
            FROM products
            GROUP BY product_id
            HAVING count > 1
        """)
        duplicate_ids = self.cursor.fetchall()
        if duplicate_ids:
            issues.append(f"Duplicate product IDs: {duplicate_ids}")
        
        return {
            'table': 'products',
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def validate_orders(self) -> Dict:
        """Validate order data"""
        issues = []
        
        # Check for NULL required fields
        self.cursor.execute("""
            SELECT order_id, customer_id, product_id, quantity, unit_price
            FROM orders
            WHERE customer_id IS NULL OR product_id IS NULL 
               OR quantity IS NULL OR unit_price IS NULL
        """)
        null_fields = self.cursor.fetchall()
        if null_fields:
            issues.append(f"Orders with NULL required fields: {null_fields}")
        
        # Check for invalid quantities
        self.cursor.execute("""
            SELECT order_id, quantity
            FROM orders
            WHERE quantity <= 0
        """)
        invalid_quantities = self.cursor.fetchall()
        if invalid_quantities:
            issues.append(f"Orders with invalid quantities: {invalid_quantities}")
        
        # Check for negative prices
        self.cursor.execute("""
            SELECT order_id, unit_price
            FROM orders
            WHERE unit_price < 0
        """)
        negative_prices = self.cursor.fetchall()
        if negative_prices:
            issues.append(f"Orders with negative prices: {negative_prices}")
        
        return {
            'table': 'orders',
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def validate_foreign_keys(self) -> Dict:
        """Validate foreign key relationships"""
        issues = []
        
        # Check for orphaned orders (customer_id doesn't exist)
        self.cursor.execute("""
            SELECT o.order_id, o.customer_id
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """)
        orphaned_customers = self.cursor.fetchall()
        if orphaned_customers:
            issues.append(f"Orders with invalid customer_id: {orphaned_customers}")
        
        # Check for orphaned orders (product_id doesn't exist)
        self.cursor.execute("""
            SELECT o.order_id, o.product_id
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.product_id
            WHERE p.product_id IS NULL
        """)
        orphaned_products = self.cursor.fetchall()
        if orphaned_products:
            issues.append(f"Orders with invalid product_id: {orphaned_products}")
        
        return {
            'constraint': 'foreign_keys',
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def validate_data_consistency(self) -> Dict:
        """Validate data consistency across tables"""
        issues = []
        
        # Check if order prices match product prices (allowing for price changes over time)
        # This is informational, not necessarily an error
        self.cursor.execute("""
            SELECT o.order_id, o.product_id, o.unit_price, p.price as current_price
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE ABS(o.unit_price - p.price) > 0.01
        """)
        price_mismatches = self.cursor.fetchall()
        if price_mismatches:
            issues.append(f"Order prices differ from current product prices (may be expected): {len(price_mismatches)} cases")
        
        # Check for orders with quantities exceeding stock (at time of order)
        # This would require historical stock tracking, so we'll just check current stock
        self.cursor.execute("""
            SELECT o.order_id, o.product_id, o.quantity, p.stock_quantity as current_stock
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.quantity > p.stock_quantity + 100  -- Allow some buffer for stock replenishment
        """)
        potential_stock_issues = self.cursor.fetchall()
        if potential_stock_issues:
            issues.append(f"Orders with quantities significantly exceeding current stock: {len(potential_stock_issues)} cases")
        
        return {
            'check': 'data_consistency',
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def run_full_validation(self) -> Dict:
        """Run complete validation suite"""
        print("=" * 60)
        print("Data Validation Report")
        print("=" * 60)
        
        self.connect()
        
        results = {
            'customers': self.validate_customers(),
            'products': self.validate_products(),
            'orders': self.validate_orders(),
            'foreign_keys': self.validate_foreign_keys(),
            'consistency': self.validate_data_consistency()
        }
        
        # Print results
        print("\n[Customers Validation]")
        print(f"  Status: {'✓ Valid' if results['customers']['valid'] else '✗ Issues Found'}")
        for issue in results['customers']['issues']:
            print(f"  - {issue}")
        
        print("\n[Products Validation]")
        print(f"  Status: {'✓ Valid' if results['products']['valid'] else '✗ Issues Found'}")
        for issue in results['products']['issues']:
            print(f"  - {issue}")
        
        print("\n[Orders Validation]")
        print(f"  Status: {'✓ Valid' if results['orders']['valid'] else '✗ Issues Found'}")
        for issue in results['orders']['issues']:
            print(f"  - {issue}")
        
        print("\n[Foreign Keys Validation]")
        print(f"  Status: {'✓ Valid' if results['foreign_keys']['valid'] else '✗ Issues Found'}")
        for issue in results['foreign_keys']['issues']:
            print(f"  - {issue}")
        
        print("\n[Data Consistency Check]")
        print(f"  Status: {'✓ Consistent' if results['consistency']['valid'] else '⚠ Warnings'}")
        for issue in results['consistency']['issues']:
            print(f"  - {issue}")
        
        # Overall status
        all_valid = all([
            results['customers']['valid'],
            results['products']['valid'],
            results['orders']['valid'],
            results['foreign_keys']['valid']
        ])
        
        print("\n" + "=" * 60)
        print(f"Overall Status: {'✓ All Validations Passed' if all_valid else '✗ Some Issues Found'}")
        print("=" * 60)
        
        self.close()
        
        return results


if __name__ == "__main__":
    validator = DataValidator()
    validator.run_full_validation()

