"""
Report Generation Module
Generates reports combining customer and product information
"""

import sqlite3
from datetime import datetime
from typing import Dict, List

class ReportGenerator:
    """Generates business reports from integrated data"""
    
    def __init__(self, db_path: str = 'integration_database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def generate_product_sales_report(self) -> List[Dict]:
        """
        Generate report showing total orders and revenue generated per product
        """
        self.cursor.execute("""
            SELECT 
                p.product_id,
                p.product_name,
                p.category,
                p.price as current_price,
                p.stock_quantity,
                COUNT(o.order_id) as total_orders,
                COALESCE(SUM(o.quantity), 0) as total_quantity_sold,
                COALESCE(SUM(o.total_amount), 0) as total_revenue,
                COALESCE(AVG(o.total_amount), 0) as average_order_value
            FROM products p
            LEFT JOIN orders o ON p.product_id = o.product_id
            GROUP BY p.product_id, p.product_name, p.category, p.price, p.stock_quantity
            ORDER BY total_revenue DESC
        """)
        
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    def generate_customer_product_report(self) -> List[Dict]:
        """
        Generate detailed report combining customer and product information
        """
        self.cursor.execute("""
            SELECT 
                c.customer_id,
                c.first_name || ' ' || c.last_name as customer_name,
                c.email,
                c.city,
                c.state,
                p.product_id,
                p.product_name,
                p.category,
                COUNT(o.order_id) as order_count,
                SUM(o.quantity) as total_quantity,
                SUM(o.total_amount) as total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state,
                     p.product_id, p.product_name, p.category
            ORDER BY c.customer_id, total_spent DESC
        """)
        
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    def generate_category_summary(self) -> List[Dict]:
        """Generate summary report by product category"""
        self.cursor.execute("""
            SELECT 
                p.category,
                COUNT(DISTINCT p.product_id) as product_count,
                COUNT(o.order_id) as total_orders,
                COALESCE(SUM(o.quantity), 0) as total_quantity_sold,
                COALESCE(SUM(o.total_amount), 0) as category_revenue,
                COALESCE(AVG(o.total_amount), 0) as average_order_value
            FROM products p
            LEFT JOIN orders o ON p.product_id = o.product_id
            GROUP BY p.category
            ORDER BY category_revenue DESC
        """)
        
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    def generate_top_customers_report(self, limit: int = 10) -> List[Dict]:
        """Generate report of top customers by revenue"""
        self.cursor.execute("""
            SELECT 
                c.customer_id,
                c.first_name || ' ' || c.last_name as customer_name,
                c.email,
                c.city,
                c.state,
                COUNT(o.order_id) as total_orders,
                SUM(o.quantity) as total_items,
                SUM(o.total_amount) as total_revenue,
                AVG(o.total_amount) as average_order_value
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
            ORDER BY total_revenue DESC
            LIMIT ?
        """, (limit,))
        
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    def print_product_sales_report(self):
        """Print formatted product sales report"""
        print("\n" + "=" * 100)
        print("PRODUCT SALES REPORT")
        print("Total Orders and Revenue Generated Per Product")
        print("=" * 100)
        
        self.connect()
        products = self.generate_product_sales_report()
        
        print(f"\n{'Product ID':<12} {'Product Name':<30} {'Category':<15} {'Orders':<8} {'Qty Sold':<10} {'Revenue':<12} {'Avg Order':<12}")
        print("-" * 100)
        
        total_revenue = 0
        for product in products:
            print(f"{product['product_id']:<12} "
                  f"{product['product_name'][:28]:<30} "
                  f"{product['category']:<15} "
                  f"{product['total_orders']:<8} "
                  f"{product['total_quantity_sold']:<10} "
                  f"${product['total_revenue']:>10.2f} "
                  f"${product['average_order_value']:>10.2f}")
            total_revenue += product['total_revenue']
        
        print("-" * 100)
        print(f"{'TOTAL':<57} ${total_revenue:>10.2f}")
        print("=" * 100)
        
        self.close()
    
    def print_customer_product_report(self):
        """Print formatted customer-product relationship report"""
        print("\n" + "=" * 120)
        print("CUSTOMER-PRODUCT INTEGRATION REPORT")
        print("Detailed Customer and Product Information")
        print("=" * 120)
        
        self.connect()
        data = self.generate_customer_product_report()
        
        print(f"\n{'Customer':<25} {'Email':<30} {'Location':<20} {'Product':<30} {'Orders':<8} {'Qty':<8} {'Spent':<12}")
        print("-" * 120)
        
        for record in data:
            location = f"{record['city']}, {record['state']}"
            print(f"{record['customer_name'][:23]:<25} "
                  f"{record['email'][:28]:<30} "
                  f"{location[:18]:<20} "
                  f"{record['product_name'][:28]:<30} "
                  f"{record['order_count']:<8} "
                  f"{record['total_quantity']:<8} "
                  f"${record['total_spent']:>10.2f}")
        
        print("=" * 120)
        
        self.close()
    
    def print_category_summary(self):
        """Print formatted category summary report"""
        print("\n" + "=" * 100)
        print("PRODUCT CATEGORY SUMMARY REPORT")
        print("=" * 100)
        
        self.connect()
        categories = self.generate_category_summary()
        
        print(f"\n{'Category':<20} {'Products':<10} {'Orders':<10} {'Qty Sold':<12} {'Revenue':<15} {'Avg Order':<12}")
        print("-" * 100)
        
        total_revenue = 0
        for category in categories:
            cat_name = category['category'] if category['category'] else 'Uncategorized'
            print(f"{cat_name[:18]:<20} "
                  f"{category['product_count']:<10} "
                  f"{category['total_orders']:<10} "
                  f"{category['total_quantity_sold']:<12} "
                  f"${category['category_revenue']:>13.2f} "
                  f"${category['average_order_value']:>10.2f}")
            total_revenue += category['category_revenue']
        
        print("-" * 100)
        print(f"{'TOTAL':<52} ${total_revenue:>13.2f}")
        print("=" * 100)
        
        self.close()
    
    def generate_full_report(self, output_file: str = 'integration_report.txt'):
        """Generate comprehensive report and save to file"""
        self.connect()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("MULTI-SOURCE DATA INTEGRATION SYSTEM - COMPREHENSIVE REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 100 + "\n\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 100 + "\n")
            
            self.cursor.execute("SELECT COUNT(*) FROM customers")
            customer_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM products")
            product_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM orders")
            order_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT SUM(total_amount) FROM orders")
            total_revenue = self.cursor.fetchone()[0] or 0
            
            f.write(f"Total Customers: {customer_count}\n")
            f.write(f"Total Products: {product_count}\n")
            f.write(f"Total Orders: {order_count}\n")
            f.write(f"Total Revenue: ${total_revenue:,.2f}\n\n")
            
            # Product Sales Report
            f.write("\n" + "=" * 100 + "\n")
            f.write("PRODUCT SALES REPORT\n")
            f.write("=" * 100 + "\n\n")
            
            products = self.generate_product_sales_report()
            f.write(f"{'Product ID':<12} {'Product Name':<30} {'Category':<15} {'Orders':<8} {'Qty Sold':<10} {'Revenue':<12}\n")
            f.write("-" * 100 + "\n")
            
            for product in products:
                f.write(f"{product['product_id']:<12} "
                       f"{product['product_name'][:28]:<30} "
                       f"{product['category']:<15} "
                       f"{product['total_orders']:<8} "
                       f"{product['total_quantity_sold']:<10} "
                       f"${product['total_revenue']:>10.2f}\n")
            
            # Category Summary
            f.write("\n" + "=" * 100 + "\n")
            f.write("CATEGORY SUMMARY\n")
            f.write("=" * 100 + "\n\n")
            
            categories = self.generate_category_summary()
            f.write(f"{'Category':<20} {'Products':<10} {'Orders':<10} {'Qty Sold':<12} {'Revenue':<15}\n")
            f.write("-" * 100 + "\n")
            
            for category in categories:
                cat_name = category['category'] if category['category'] else 'Uncategorized'
                f.write(f"{cat_name[:18]:<20} "
                       f"{category['product_count']:<10} "
                       f"{category['total_orders']:<10} "
                       f"{category['total_quantity_sold']:<12} "
                       f"${category['category_revenue']:>13.2f}\n")
            
            # Top Customers
            f.write("\n" + "=" * 100 + "\n")
            f.write("TOP 10 CUSTOMERS BY REVENUE\n")
            f.write("=" * 100 + "\n\n")
            
            top_customers = self.generate_top_customers_report(10)
            f.write(f"{'Customer Name':<30} {'Email':<30} {'Orders':<8} {'Total Revenue':<15}\n")
            f.write("-" * 100 + "\n")
            
            for customer in top_customers:
                f.write(f"{customer['customer_name'][:28]:<30} "
                       f"{customer['email'][:28]:<30} "
                       f"{customer['total_orders']:<8} "
                       f"${customer['total_revenue']:>13.2f}\n")
        
        self.close()
        print(f"\nFull report saved to: {output_file}")
    
    def print_all_reports(self):
        """Print all reports to console"""
        self.print_product_sales_report()
        self.print_category_summary()
        self.print_customer_product_report()
        
        # Generate and save full report
        self.generate_full_report()


if __name__ == "__main__":
    generator = ReportGenerator()
    generator.print_all_reports()

