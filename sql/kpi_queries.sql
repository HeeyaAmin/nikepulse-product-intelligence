-- 1. Revenue by region
SELECT
    region,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(price_per_unit), 2) AS avg_price_per_unit
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;


-- 2. Revenue by retailer
SELECT
    retailer,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold
FROM sales
GROUP BY retailer
ORDER BY total_revenue DESC;


-- 3. Sales method performance
SELECT
    sales_method,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold,
    COUNT(*) AS transaction_count
FROM sales
GROUP BY sales_method
ORDER BY total_revenue DESC;


-- 4. Top-selling products
SELECT
    product_name,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(price_per_unit), 2) AS avg_price
FROM sales
GROUP BY product_name
ORDER BY total_units_sold DESC
LIMIT 10;


-- 5. Review sentiment distribution
SELECT
    rating_group,
    COUNT(*) AS review_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM reviews
GROUP BY rating_group
ORDER BY review_count DESC;


-- 6. Average rating by product
SELECT
    product_name,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS total_reviews
FROM reviews
GROUP BY product_name
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC;


-- 7. Low-rated products needing attention
SELECT
    product_name,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS total_reviews
FROM reviews
GROUP BY product_name
HAVING AVG(rating) < 3.5
ORDER BY avg_rating ASC;


-- 8. Monthly revenue trend
SELECT
    DATE_TRUNC('month', sale_date) AS sales_month,
    SUM(revenue) AS monthly_revenue,
    SUM(quantity) AS monthly_units_sold
FROM sales
GROUP BY DATE_TRUNC('month', sale_date)
ORDER BY sales_month;


-- 9. Product performance summary from sales
SELECT
    product_name,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(price_per_unit), 2) AS avg_price_per_unit,
    COUNT(*) AS transaction_count
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC;