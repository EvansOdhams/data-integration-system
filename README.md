# Multi-Source Data Integration System

A comprehensive database solution that integrates customer and product data from multiple sources into a centralized database system.

## 🚀 Web Application (Streamlit + Supabase)

This project includes a **web-based UI** built with **Streamlit** and **Supabase** for online submission and demonstration.

- **Streamlit UI**: Interactive web interface for all features
- **Supabase Database**: Cloud-hosted PostgreSQL database
- **Real-time Integration**: Import and visualize data in real-time
- **Interactive Reports**: Dynamic charts and visualizations

See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed setup instructions.

## Project Overview

This project demonstrates the integration of data from two distinct sources:
- **Customer Data System**: Relational database containing customer information
- **Product Data System**: External CSV file containing product information

The system provides a unified database schema, data integration scripts, validation mechanisms, query examples, and reporting capabilities.

## Project Structure

```
.
├── app.py                      # Streamlit web application (main UI)
├── requirements.txt            # Python dependencies
├── schema_supabase.sql         # PostgreSQL schema for Supabase
├── supabase_integration.py     # Supabase data integration script
├── SUPABASE_SETUP.md           # Supabase setup guide
├── env_example.txt             # Environment variables template
│
├── schema.sql                  # SQLite schema definition (DDL)
├── customer_data.sql           # Sample customer data (from Customer Data System)
├── product_data.csv            # Sample product data (from Product Data System)
├── data_integration.py         # SQLite integration script
├── data_validation.py          # Data validation and integrity checks
├── queries.sql                 # SQL queries demonstrating integration
├── report_generator.py         # Report generation module
├── run_queries.py              # Query execution script
├── schema_diagram.md           # ERD and schema documentation
├── README.md                   # This file
└── mini_project_doc.md         # Project requirements document
```

## Features

### Database Design
- Normalized relational schema with three main tables: `customers`, `products`, and `orders`
- Foreign key relationships ensuring referential integrity
- CHECK constraints for data validation
- Indexes for query optimization
- Generated columns for calculated fields

### Data Integration
- Import customer data from SQL source
- Import product data from CSV file
- Automatic foreign key validation
- Data type conversion and cleaning
- Error handling for invalid records

### Data Validation
- Customer data validation (required fields, email format, duplicates)
- Product data validation (prices, stock quantities)
- Order data validation (quantities, prices)
- Foreign key integrity checks
- Data consistency validation

### Query Capabilities
- Customer details with ordered products
- Total order value per customer
- Product filtering by price range
- Customers with orders exceeding thresholds
- Additional analytical queries

### Report Generation
- Product sales reports (orders and revenue per product)
- Customer-product integration reports
- Category summaries
- Top customers analysis
- Comprehensive text-based reports

## Prerequisites

### For Web Application (Streamlit + Supabase)
- Python 3.7 or higher
- Supabase account (free tier available)
- Streamlit and Supabase packages (see requirements.txt)

### For Local SQLite Version
- Python 3.7 or higher
- SQLite3 (included with Python)
- No additional packages required (uses only standard library)

## Setup and Installation

### Option 1: Web Application (Recommended for Submission)

1. **Create Supabase Account**
   - Go to [supabase.com](https://supabase.com) and create a free account
   - Create a new project
   - Follow instructions in [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your Supabase credentials (see SUPABASE_SETUP.md)

4. **Run Streamlit Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Application**
   - Open browser to `http://localhost:8501`
   - Navigate through different pages using the sidebar

### Option 2: Local SQLite Version

1. **Clone or download the project files**

2. **Ensure all files are in the same directory**:
   - `schema.sql`
   - `customer_data.sql`
   - `product_data.csv`
   - `data_integration.py`
   - `data_validation.py`
   - `queries.sql`
   - `report_generator.py`

3. **No additional installation required** - the project uses only Python standard library modules.

## Usage

### Step 1: Run Data Integration

Execute the main integration script to create the database and import all data:

```bash
python data_integration.py
```

This will:
- Create the database schema
- Import customer data from `customer_data.sql`
- Import product data from `product_data.csv`
- Create sample order data
- Validate data integrity
- Generate a database file: `integration_database.db`

### Step 2: Run Data Validation

Verify data integrity and consistency:

```bash
python data_validation.py
```

This will check:
- Required fields
- Data constraints
- Foreign key relationships
- Data consistency

### Step 3: Execute SQL Queries

**Option 1: Using Python script (Recommended - Cross-platform)**

```bash
python run_queries.py
```

**Option 2: Using SQLite command line**

**For Windows PowerShell:**
```powershell
Get-Content queries.sql | sqlite3 integration_database.db
```

Or using the `.read` command:
```powershell
sqlite3 integration_database.db ".read queries.sql"
```

**For Linux/Mac (Bash):**
```bash
sqlite3 integration_database.db < queries.sql
```

**Option 3: Using Python directly**

```python
import sqlite3
conn = sqlite3.connect('integration_database.db')
cursor = conn.cursor()

# Read and execute queries
with open('queries.sql', 'r') as f:
    queries = f.read()
    cursor.executescript(queries)
```

### Step 4: Generate Reports

Generate comprehensive reports:

```bash
python report_generator.py
```

This will:
- Display product sales reports
- Show category summaries
- Display customer-product integration reports
- Save a comprehensive report to `integration_report.txt`

## Database Schema

### Tables

1. **customers**
   - Customer information from the Customer Data System
   - Fields: customer_id, name, email, address, contact details

2. **products**
   - Product information from the Product Data System
   - Fields: product_id, name, price, stock_quantity, category

3. **orders**
   - Links customers and products
   - Fields: order_id, customer_id, product_id, order_date, quantity, pricing

See `schema_diagram.md` for detailed ERD and schema documentation.

## Key Queries

### 1. Customer Details with Products Ordered
```sql
SELECT c.*, p.product_name, o.quantity, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id;
```

### 2. Total Order Value Per Customer
```sql
SELECT c.customer_id, c.first_name || ' ' || c.last_name AS name,
       SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

### 3. Products by Price Range
```sql
SELECT * FROM products
WHERE price BETWEEN 50.00 AND 200.00;
```

### 4. Customers with Orders Exceeding Amount
```sql
SELECT c.*, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING SUM(o.total_amount) > 1000.00;
```

## Data Validation

The system includes comprehensive validation:

- **Required Fields**: Ensures all mandatory fields are present
- **Data Types**: Validates correct data types and formats
- **Constraints**: Enforces CHECK constraints (prices, quantities)
- **Foreign Keys**: Validates referential integrity
- **Business Rules**: Checks for logical consistency

## Report Examples

### Product Sales Report
Shows total orders and revenue generated per product, sorted by revenue.

### Category Summary
Groups products by category and shows aggregate sales metrics.

### Customer-Product Integration Report
Detailed view of customer purchases with product information.

## Extending the System

### Adding New Data Sources

1. Create a new import method in `data_integration.py`
2. Add validation rules in `data_validation.py`
3. Update schema if new tables/fields are needed

### Custom Queries

Add your queries to `queries.sql` or create new query files.

### Custom Reports

Extend `report_generator.py` with new report methods.

## Troubleshooting

### Database File Not Found
- Ensure you've run `data_integration.py` first
- Check that `integration_database.db` exists in the project directory

### Import Errors
- Verify that `customer_data.sql` and `product_data.csv` exist
- Check file paths and permissions
- Review error messages for specific validation failures

### Foreign Key Violations
- Ensure customer and product data is imported before creating orders
- Check that referenced IDs exist in parent tables

## Project Deliverables Summary

✅ **Database Schema Design**: Complete ERD and schema in `schema.sql` and `schema_diagram.md`

✅ **Working Implementation**: 
   - `data_integration.py` - Integrates both data sources
   - Database creation and population scripts

✅ **SQL Queries**: Comprehensive queries in `queries.sql` demonstrating:
   - Customer details with products
   - Total order values
   - Price filtering
   - High-value customers

✅ **Data Validation**: `data_validation.py` ensures data consistency and integrity

✅ **Report Generation**: `report_generator.py` creates comprehensive business reports

✅ **Documentation**: Complete README and schema documentation

## Author

Created as part of CSC 802 - Systems and Data Integration course project.

## License

This project is for educational purposes.

