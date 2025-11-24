"""
Multi-Source Data Integration System - Streamlit Web Application
Main application file for the web UI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
import os
from dotenv import load_dotenv
import json

from typing import Optional

from sample_data import SAMPLE_CUSTOMERS, SAMPLE_PRODUCTS, SAMPLE_ORDERS

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Source Data Integration System",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    """Initialize Supabase client"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        st.error("⚠️ Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in .env file")
        return None
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        return supabase
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        return None

# Sidebar navigation
st.sidebar.title("🔗 Data Integration System")
page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "📊 Database Schema", "🔄 Data Integration", "📝 SQL Queries", "📈 Reports", "✅ Data Validation"]
)

supabase = init_supabase()

# Pre-load sample dataframes for fallback display
SAMPLE_DATAFRAMES = {
    "customers": pd.DataFrame(SAMPLE_CUSTOMERS),
    "products": pd.DataFrame(SAMPLE_PRODUCTS),
    "orders": pd.DataFrame(SAMPLE_ORDERS),
}


def get_table_dataframe(table_name: str, limit: Optional[int] = None, show_warning: bool = False):
    """
    Fetch table data from Supabase if available, otherwise use local sample data.

    Returns:
        tuple[pd.DataFrame, str]: dataframe and data source ("supabase" or "sample")
    """
    if supabase:
        try:
            query = supabase.table(table_name).select("*")
            if limit:
                query = query.limit(limit)
            result = query.execute()
            if result.data:
                df = pd.DataFrame(result.data)
                if limit:
                    df = df.head(limit)
                return df, "supabase"
        except Exception as e:
            if show_warning:
                st.warning(f"Could not load {table_name} from Supabase: {e}")

    df = SAMPLE_DATAFRAMES[table_name].copy()
    if limit:
        df = df.head(limit)
    return df, "sample"


def notify_sample_data(source: str):
    """Show info message if sample data is being displayed."""
    if source == "sample":
        st.info(
            "Showing built-in sample data. Configure Supabase and run the data "
            "integration steps to work with your own live database."
        )

# Home Page
if page == "🏠 Home":
    st.title("Multi-Source Data Integration System")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the Data Integration System
    
    This application demonstrates the integration of data from multiple sources into a centralized database:
    
    - **Customer Data System**: Relational database with customer information
    - **Product Data System**: External CSV file with product data
    
    ### Features
    
    - 📊 **Database Schema**: View ERD and schema design
    - 🔄 **Data Integration**: Import data from multiple sources
    - 📝 **SQL Queries**: Execute queries and view results
    - 📈 **Reports**: Generate comprehensive business reports
    - ✅ **Data Validation**: Ensure data integrity and consistency
    
    ### Getting Started
    
    1. Navigate to **Database Schema** to view the database design
    2. Go to **Data Integration** to import data from sources
    3. Use **SQL Queries** to explore the integrated data
    4. Generate **Reports** for business insights
    5. Run **Data Validation** to ensure data quality
    """)
    
    customers_df, customers_source = get_table_dataframe("customers")
    products_df, products_source = get_table_dataframe("products")
    orders_df, orders_source = get_table_dataframe("orders")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Customers", len(customers_df))
    with col2:
        st.metric("Products", len(products_df))
    with col3:
        st.metric("Orders", len(orders_df))

    if supabase and customers_source == products_source == orders_source == "supabase":
        st.success("✅ Connected to Supabase database")
    else:
        notify_sample_data("sample")

# Database Schema Page
elif page == "📊 Database Schema":
    st.title("Database Schema Design")
    st.markdown("---")
    
    st.markdown("""
    ### Entity Relationship Diagram (ERD)
    
    The database consists of three main tables:
    """)
    
    # Schema visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Customers Table
        - **Primary Key**: customer_id
        - **Fields**: first_name, last_name, email, phone, address, city, state, zip_code, country
        - **Source**: Customer Data System (Relational Database)
        """)
        
        st.markdown("""
        #### Products Table
        - **Primary Key**: product_id
        - **Fields**: product_name, description, price, stock_quantity, category, supplier
        - **Source**: Product Data System (CSV/API)
        """)
    
    with col2:
        st.markdown("""
        #### Orders Table
        - **Primary Key**: order_id
        - **Foreign Keys**: customer_id → customers, product_id → products
        - **Fields**: order_date, quantity, unit_price, total_amount (generated), status
        - **Purpose**: Links customers and products
        """)
        
        st.markdown("""
        #### Relationships
        - Customers → Orders (One-to-Many)
        - Products → Orders (One-to-Many)
        """)
    
    # ERD Diagram (ASCII/Text representation)
    st.markdown("### ERD Diagram")
    st.code("""
    ┌─────────────────┐
    │   CUSTOMERS     │
    ├─────────────────┤
    │ PK customer_id  │
    │    first_name   │
    │    last_name    │
    │    email        │
    │    address      │
    └────────┬────────┘
             │ 1
             │
             │ N
    ┌────────┴────────┐
    │     ORDERS      │
    ├─────────────────┤
    │ PK order_id     │
    │ FK customer_id ─┼──┐
    │ FK product_id ──┼──┼──┐
    │    order_date   │  │  │
    │    quantity     │  │  │
    │    total_amount │  │  │
    └─────────────────┘  │  │
             │            │  │
             │ N          │  │
             │            │  │
             │ 1          │  │
    ┌────────┴────────────┘  │
    │      PRODUCTS          │
    ├─────────────────────────┤
    │ PK product_id          │
    │    product_name         │
    │    price                │
    │    stock_quantity       │
    │    category             │
    └─────────────────────────┘
    """, language="text")
    
    # Show actual schema (Supabase or sample fallback)
    st.markdown("### Current Database Tables")
    tables = ['customers', 'products', 'orders']
    schema_using_sample = False
    for table in tables:
        df, source = get_table_dataframe(table, limit=1)
        with st.expander(f"📋 {table.upper()} Table Structure"):
            if not df.empty:
                st.dataframe(df.head(0))  # display column headers
                st.info(f"Columns: {', '.join(df.columns.tolist())}")
            else:
                st.warning("No data available. Run the data integration step.")
        if source == "sample":
            schema_using_sample = True
    if schema_using_sample:
        notify_sample_data("sample")

# Data Integration Page
elif page == "🔄 Data Integration":
    st.title("Data Integration")
    st.markdown("---")
    
    supabase_ready = supabase is not None
    if not supabase_ready:
        st.warning("Supabase is not configured. Buttons are disabled, but you can preview the built-in sample data.")
    
    st.markdown("""
    ### Import Data from Multiple Sources
    
    This section allows you to integrate data from:
    - **Customer Data System**: SQL file with customer records
    - **Product Data System**: CSV file with product information
    """)
    
    tab1, tab2, tab3 = st.tabs(["Import Customers", "Import Products", "Create Orders"])
    
    with tab1:
        st.subheader("Import Customer Data")
        st.info("Customer data is imported from the Customer Data System (SQL file)")
        
        if st.button("Import Customer Data", type="primary", disabled=not supabase_ready):
            try:
                from supabase_integration import SupabaseIntegrator
                integrator = SupabaseIntegrator()
                integrator.import_customer_data()
                st.success("✅ Customer data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing customer data: {e}")
        
        # Show current customers
        df_customers, source = get_table_dataframe("customers")
        st.dataframe(df_customers, use_container_width=True)
        st.info(f"Total customers: {len(df_customers)}")
        if source == "sample":
            notify_sample_data(source)
    
    with tab2:
        st.subheader("Import Product Data")
        st.info("Product data is imported from the Product Data System (CSV file)")
        
        if st.button("Import Product Data", type="primary", disabled=not supabase_ready):
            try:
                from supabase_integration import SupabaseIntegrator
                integrator = SupabaseIntegrator()
                integrator.import_product_data()
                st.success("✅ Product data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing product data: {e}")
        
        # Show current products
        df_products, source = get_table_dataframe("products")
        st.dataframe(df_products, use_container_width=True)
        st.info(f"Total products: {len(df_products)}")
        if source == "sample":
            notify_sample_data(source)
    
    with tab3:
        st.subheader("Create Sample Orders")
        st.info("Create sample order data to link customers and products")
        
        if st.button("Create Sample Orders", type="primary", disabled=not supabase_ready):
            try:
                from supabase_integration import SupabaseIntegrator
                integrator = SupabaseIntegrator()
                integrator.create_sample_orders()
                st.success("✅ Sample orders created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating orders: {e}")
        
        # Show current orders
        df_orders, source = get_table_dataframe("orders")
        st.dataframe(df_orders, use_container_width=True)
        st.info(f"Total orders: {len(df_orders)}")
        if source == "sample":
            notify_sample_data(source)

# SQL Queries Page
elif page == "📝 SQL Queries":
    st.title("SQL Queries")
    st.markdown("---")
    
    # Predefined queries
    queries = {
        "Customer Details with Products Ordered": """
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            p.product_name,
            o.quantity,
            o.total_amount
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN products p ON o.product_id = p.product_id
        ORDER BY c.customer_id;
        """,
        "Total Order Value Per Customer": """
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.total_amount) AS total_order_value
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_order_value DESC NULLS LAST;
        """,
        "Products by Price Range ($50-$200)": """
        SELECT 
            product_id,
            product_name,
            category,
            price,
            stock_quantity
        FROM products
        WHERE price BETWEEN 50.00 AND 200.00
        ORDER BY price ASC;
        """,
        "Customers with Orders Exceeding $1000": """
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            SUM(o.total_amount) AS total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        HAVING SUM(o.total_amount) > 1000.00
        ORDER BY total_spent DESC;
        """
    }
    
    query_choice = st.selectbox("Select a predefined query:", list(queries.keys()))
    
    query = st.text_area("SQL Query:", queries[query_choice], height=200)
    
    if st.button("Execute Query", type="primary"):
        data_sources = set()
        try:
            # Note: Supabase client doesn't support raw SQL directly
            # We'll use table methods (Supabase or sample fallback) to simulate query results
            st.info("💡 Showing query results using available data. Configure Supabase for live execution.")
            
            # Execute based on query type
            if "Customer Details with Products" in query_choice:
                df_customers, src = get_table_dataframe("customers")
                data_sources.add(src)
                df_orders, src = get_table_dataframe("orders")
                data_sources.add(src)
                df_products, src = get_table_dataframe("products")
                data_sources.add(src)
                
                if not df_orders.empty:
                    merged = df_orders.merge(df_customers, on='customer_id', how='inner')
                    merged = merged.merge(df_products, on='product_id', how='inner')
                    merged['customer_name'] = merged['first_name'] + ' ' + merged['last_name']
                    
                    result_df = merged[['customer_id', 'customer_name', 'email', 'product_name', 'quantity', 'total_amount']]
                    st.dataframe(result_df, use_container_width=True)
                    st.success(f"✅ Returned {len(result_df)} rows")
                else:
                    st.warning("No orders found")
            
            elif "Total Order Value" in query_choice:
                df_customers, src = get_table_dataframe("customers")
                data_sources.add(src)
                df_orders, src = get_table_dataframe("orders")
                data_sources.add(src)
                
                if not df_orders.empty:
                    merged = df_orders.merge(df_customers, on='customer_id', how='right')
                    summary = merged.groupby(['customer_id', 'first_name', 'last_name']).agg({
                        'order_id': 'count',
                        'total_amount': 'sum'
                    }).reset_index()
                    summary['customer_name'] = summary['first_name'] + ' ' + summary['last_name']
                    summary = summary[['customer_id', 'customer_name', 'order_id', 'total_amount']]
                    summary.columns = ['Customer ID', 'Customer Name', 'Total Orders', 'Total Order Value']
                    summary = summary.sort_values('Total Order Value', ascending=False, na_position='last')
                    
                    st.dataframe(summary, use_container_width=True)
                    st.success(f"✅ Returned {len(summary)} rows")
                else:
                    st.warning("No orders found")
            
            elif "Price Range" in query_choice:
                df_products, src = get_table_dataframe("products")
                data_sources.add(src)
                
                if not df_products.empty:
                    filtered = df_products[(df_products['price'] >= 50) & (df_products['price'] <= 200)]
                    filtered = filtered[['product_id', 'product_name', 'category', 'price', 'stock_quantity']]
                    filtered = filtered.sort_values('price')
                    
                    st.dataframe(filtered, use_container_width=True)
                    st.success(f"✅ Returned {len(filtered)} rows")
                else:
                    st.warning("No products found")
            
            elif "Orders Exceeding" in query_choice:
                df_customers, src = get_table_dataframe("customers")
                data_sources.add(src)
                df_orders, src = get_table_dataframe("orders")
                data_sources.add(src)
                
                if not df_orders.empty:
                    merged = df_orders.merge(df_customers, on='customer_id', how='inner')
                    summary = merged.groupby(['customer_id', 'first_name', 'last_name', 'email']).agg({
                        'total_amount': 'sum'
                    }).reset_index()
                    summary = summary[summary['total_amount'] > 1000]
                    summary['customer_name'] = summary['first_name'] + ' ' + summary['last_name']
                    summary = summary[['customer_id', 'customer_name', 'email', 'total_amount']]
                    summary.columns = ['Customer ID', 'Customer Name', 'Email', 'Total Spent']
                    summary = summary.sort_values('Total Spent', ascending=False)
                    
                    st.dataframe(summary, use_container_width=True)
                    st.success(f"✅ Returned {len(summary)} rows")
                else:
                    st.warning("No orders found")
            
        except Exception as e:
            st.error(f"Error executing query: {e}")
            st.info("💡 Tip: For complex queries, use Supabase SQL Editor or create RPC functions")
        finally:
            if "sample" in data_sources:
                notify_sample_data("sample")

# Reports Page
elif page == "📈 Reports":
    st.title("Business Reports")
    st.markdown("---")
    
    try:
        df_products, src_products = get_table_dataframe("products")
        df_orders, src_orders = get_table_dataframe("orders")
        df_customers, src_customers = get_table_dataframe("customers")
        data_sources = {src_products, src_orders, src_customers}
        if "sample" in data_sources:
            notify_sample_data("sample")

        # Product Sales Report
        st.subheader("📊 Product Sales Report")
        
        if not df_orders.empty and not df_products.empty:
            # Merge and aggregate
            product_sales = df_orders.merge(df_products, on='product_id', how='right')
            sales_summary = product_sales.groupby(['product_id', 'product_name', 'category']).agg({
                'order_id': 'count',
                'quantity': 'sum',
                'total_amount': 'sum'
            }).reset_index()
            sales_summary.columns = ['Product ID', 'Product Name', 'Category', 'Total Orders', 'Total Quantity', 'Total Revenue']
            
            st.dataframe(sales_summary.sort_values('Total Revenue', ascending=False), use_container_width=True)
            
            # Visualization
            fig = px.bar(sales_summary.head(10), x='Product Name', y='Total Revenue', 
                        title='Top 10 Products by Revenue', color='Category')
            st.plotly_chart(fig, use_container_width=True)
        
        # Category Summary
        st.subheader("📁 Category Summary")
        
        if not df_orders.empty and not df_products.empty:
            category_summary = product_sales.groupby('category').agg({
                'product_id': 'nunique',
                'order_id': 'count',
                'total_amount': 'sum'
            }).reset_index()
            category_summary.columns = ['Category', 'Products', 'Orders', 'Revenue']
            
            st.dataframe(category_summary.sort_values('Revenue', ascending=False), use_container_width=True)
            
            # Pie chart
            fig = px.pie(category_summary, values='Revenue', names='Category', 
                        title='Revenue by Category')
            st.plotly_chart(fig, use_container_width=True)
        
        # Customer Summary
        st.subheader("👥 Customer Summary")
        
        if not df_orders.empty and not df_customers.empty:
            customer_orders = df_orders.merge(df_customers, on='customer_id', how='inner')
            customer_summary = customer_orders.groupby(['customer_id', 'first_name', 'last_name']).agg({
                'order_id': 'count',
                'total_amount': 'sum'
            }).reset_index()
            customer_summary['customer_name'] = customer_summary['first_name'] + ' ' + customer_summary['last_name']
            customer_summary = customer_summary[['customer_name', 'order_id', 'total_amount']]
            customer_summary.columns = ['Customer Name', 'Total Orders', 'Total Spent']
            
            st.dataframe(customer_summary.sort_values('Total Spent', ascending=False), use_container_width=True)
            
    except Exception as e:
        st.error(f"Error generating reports: {e}")

# Data Validation Page
elif page == "✅ Data Validation":
    st.title("Data Validation")
    st.markdown("---")
    
    if st.button("Run Data Validation", type="primary"):
        try:
            df_customers, src_customers = get_table_dataframe("customers")
            df_products, src_products = get_table_dataframe("products")
            df_orders, src_orders = get_table_dataframe("orders")
            data_sources = {src_customers, src_products, src_orders}
            if "sample" in data_sources:
                notify_sample_data("sample")
            
            st.success("✅ Data validation completed!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Customers", len(df_customers))
                if not df_customers.empty:
                    null_emails = df_customers['email'].isna().sum()
                    if null_emails == 0:
                        st.success("✅ All customers have emails")
                    else:
                        st.warning(f"⚠️ {null_emails} customers missing emails")
            
            with col2:
                st.metric("Products", len(df_products))
                if not df_products.empty:
                    negative_prices = (df_products['price'] < 0).sum()
                    if negative_prices == 0:
                        st.success("✅ All products have valid prices")
                    else:
                        st.warning(f"⚠️ {negative_prices} products with negative prices")
            
            with col3:
                st.metric("Orders", len(df_orders))
                if not df_orders.empty:
                    invalid_quantities = (df_orders['quantity'] <= 0).sum()
                    if invalid_quantities == 0:
                        st.success("✅ All orders have valid quantities")
                    else:
                        st.warning(f"⚠️ {invalid_quantities} orders with invalid quantities")
            
            # Foreign key validation
            st.subheader("Foreign Key Validation")
            if not df_orders.empty:
                valid_customers = df_orders['customer_id'].isin(df_customers['customer_id']).all()
                valid_products = df_orders['product_id'].isin(df_products['product_id']).all()
                
                if valid_customers and valid_products:
                    st.success("✅ All foreign key relationships are valid")
                else:
                    if not valid_customers:
                        st.error("❌ Some orders reference invalid customers")
                    if not valid_products:
                        st.error("❌ Some orders reference invalid products")
        
        except Exception as e:
            st.error(f"Error during validation: {e}")

