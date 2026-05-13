-- Count rows in each table
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
UNION ALL
SELECT 'sales' AS table_name, COUNT(*) AS row_count FROM sales
UNION ALL
SELECT 'reviews' AS table_name, COUNT(*) AS row_count FROM reviews;


-- Check missing product names in sales
SELECT COUNT(*) AS missing_product_names
FROM sales
WHERE product_name IS NULL OR product_name = '';


-- Check missing sales dates
SELECT COUNT(*) AS missing_sale_dates
FROM sales
WHERE sale_date IS NULL;


-- Check negative or zero revenue
SELECT COUNT(*) AS invalid_revenue_rows
FROM sales
WHERE revenue <= 0 OR revenue IS NULL;


-- Check invalid ratings
SELECT COUNT(*) AS invalid_rating_rows
FROM reviews
WHERE rating < 1 OR rating > 5 OR rating IS NULL;


-- Check duplicate product IDs
SELECT product_id, COUNT(*) AS duplicate_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;