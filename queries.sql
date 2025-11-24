-- Multi-Source Data Integration System
-- SQL Queries Demonstrating Integration and Insights Retrieval

-- ============================================================================
-- QUERY 1: Fetch customer details along with the products they ordered
-- ============================================================================
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.city,
    c.state,
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    o.quantity,
    o.unit_price,
    o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id
ORDER BY c.customer_id, o.order_date DESC;

-- Alternative using the order_summary view
SELECT * FROM order_summary
ORDER BY customer_id, order_date DESC;

-- ============================================================================
-- QUERY 2: Calculate total value of orders per customer
-- ============================================================================
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS total_items_ordered,
    SUM(o.total_amount) AS total_order_value,
    AVG(o.total_amount) AS average_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
ORDER BY total_order_value DESC NULLS LAST;

-- ============================================================================
-- QUERY 3: Filter products by price range
-- ============================================================================
-- Products between $50 and $200
SELECT 
    product_id,
    product_name,
    category,
    price,
    stock_quantity,
    supplier
FROM products
WHERE price BETWEEN 50.00 AND 200.00
ORDER BY price ASC;

-- Products under $50
SELECT 
    product_id,
    product_name,
    category,
    price,
    stock_quantity
FROM products
WHERE price < 50.00
ORDER BY price ASC;

-- Products over $500
SELECT 
    product_id,
    product_name,
    category,
    price,
    stock_quantity
FROM products
WHERE price > 500.00
ORDER BY price DESC;

-- ============================================================================
-- QUERY 4: Identify customers with orders exceeding a certain amount
-- ============================================================================
-- Customers with total order value exceeding $1000
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.city,
    c.state,
    COUNT(o.order_id) AS number_of_orders,
    SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
HAVING SUM(o.total_amount) > 1000.00
ORDER BY total_spent DESC;

-- Customers with any single order exceeding $500
SELECT DISTINCT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 500.00
ORDER BY o.total_amount DESC;

-- ============================================================================
-- ADDITIONAL USEFUL QUERIES
-- ============================================================================

-- Top 5 best-selling products by quantity
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS total_quantity_sold,
    COUNT(o.order_id) AS number_of_orders,
    SUM(o.total_amount) AS total_revenue
FROM products p
JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_quantity_sold DESC
LIMIT 5;

-- Products with low stock (less than 50 units)
SELECT 
    product_id,
    product_name,
    category,
    stock_quantity,
    price
FROM products
WHERE stock_quantity < 50
ORDER BY stock_quantity ASC;

-- Monthly sales summary
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS total_items_sold,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month DESC;

-- Customer order history with product details (detailed view)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    o.quantity,
    o.unit_price,
    o.total_amount,
    o.status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE c.customer_id = 1  -- Replace with specific customer ID
ORDER BY o.order_date DESC;

-- Revenue by product category
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) AS products_in_category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS total_quantity_sold,
    SUM(o.total_amount) AS category_revenue,
    AVG(o.total_amount) AS average_order_value
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.category
ORDER BY category_revenue DESC NULLS LAST;

-- Customers who haven't placed any orders
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.city,
    c.state
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

