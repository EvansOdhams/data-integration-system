# Database Schema Design

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────┐
│         CUSTOMERS               │
├─────────────────────────────────┤
│ PK customer_id (INT)            │
│    first_name (VARCHAR)         │
│    last_name (VARCHAR)          │
│    email (VARCHAR) UNIQUE       │
│    phone (VARCHAR)              │
│    address (VARCHAR)            │
│    city (VARCHAR)               │
│    state (VARCHAR)              │
│    zip_code (VARCHAR)           │
│    country (VARCHAR)            │
│    created_at (TIMESTAMP)       │
│    updated_at (TIMESTAMP)       │
└─────────────────────────────────┘
            │
            │ 1
            │
            │ N
┌───────────┴─────────────────────┐
│            ORDERS                │
├──────────────────────────────────┤
│ PK order_id (INT)                │
│ FK customer_id (INT) ────────────┼──┐
│ FK product_id (INT) ─────────────┼──┼──┐
│    order_date (DATE)             │  │  │
│    quantity (INT)                │  │  │
│    unit_price (DECIMAL)          │  │  │
│    total_amount (GENERATED)       │  │  │
│    status (VARCHAR)              │  │  │
│    created_at (TIMESTAMP)        │  │  │
└──────────────────────────────────┘  │  │
            │                         │  │
            │ N                       │  │
            │                         │  │
            │ 1                       │  │
┌───────────┴─────────────────────────┘  │
│         PRODUCTS                       │
├─────────────────────────────────────────┤
│ PK product_id (INT)                    │
│    product_name (VARCHAR)               │
│    description (TEXT)                   │
│    price (DECIMAL)                      │
│    stock_quantity (INT)                 │
│    category (VARCHAR)                   │
│    supplier (VARCHAR)                   │
│    created_at (TIMESTAMP)               │
│    updated_at (TIMESTAMP)               │
└─────────────────────────────────────────┘
```

## Schema Description

### Tables

#### 1. **customers**
Represents customer data imported from the Customer Data System (relational database source).

- **Primary Key**: `customer_id`
- **Unique Constraint**: `email`
- **Key Fields**:
  - Customer identification and contact information
  - Address details for shipping/billing
  - Timestamps for audit trail

#### 2. **products**
Represents product data imported from the Product Data System (external API/CSV source).

- **Primary Key**: `product_id`
- **Constraints**:
  - `price >= 0` (CHECK constraint)
  - `stock_quantity >= 0` (CHECK constraint)
- **Key Fields**:
  - Product information and pricing
  - Inventory management (stock_quantity)
  - Categorization and supplier information

#### 3. **orders**
Links customers and products, representing transactions/orders.

- **Primary Key**: `order_id`
- **Foreign Keys**:
  - `customer_id` → `customers(customer_id)` (CASCADE DELETE)
  - `product_id` → `products(product_id)` (CASCADE DELETE)
- **Constraints**:
  - `quantity > 0` (CHECK constraint)
  - `unit_price >= 0` (CHECK constraint)
- **Computed Field**: `total_amount` = `quantity * unit_price` (STORED GENERATED)
- **Key Fields**:
  - Order details and quantities
  - Pricing information (captured at time of order)
  - Order status tracking

### Relationships

1. **Customers → Orders** (One-to-Many)
   - One customer can have multiple orders
   - Each order belongs to exactly one customer
   - Foreign key: `orders.customer_id` references `customers.customer_id`

2. **Products → Orders** (One-to-Many)
   - One product can appear in multiple orders
   - Each order line item references exactly one product
   - Foreign key: `orders.product_id` references `products.product_id`

### Indexes

For performance optimization, indexes are created on:
- `orders(customer_id)` - Fast customer order lookups
- `orders(product_id)` - Fast product order lookups
- `orders(order_date)` - Date range queries
- `customers(email)` - Email lookups
- `products(price)` - Price range filtering
- `products(category)` - Category-based queries

### Views

**order_summary**: A convenient view that joins all three tables to provide a complete order overview with customer and product details.

## Data Flow

```
┌─────────────────────┐
│ Customer Data       │
│ System (SQL)        │──┐
└─────────────────────┘  │
                         │
                         ├──► [Data Integration] ──► [Centralized Database]
                         │
┌─────────────────────┐  │
│ Product Data        │  │
│ System (CSV/API)    │──┘
└─────────────────────┘
```

## Integration Points

1. **Customer Data Integration**
   - Source: SQL file (`customer_data.sql`)
   - Method: Direct SQL INSERT statements
   - Validation: Email uniqueness, required fields

2. **Product Data Integration**
   - Source: CSV file (`product_data.csv`)
   - Method: CSV parsing and INSERT statements
   - Validation: Price/quantity constraints, data type conversion

3. **Order Data Creation**
   - Source: Generated sample data
   - Method: SQL INSERT with foreign key validation
   - Validation: Foreign key existence, constraint checks

