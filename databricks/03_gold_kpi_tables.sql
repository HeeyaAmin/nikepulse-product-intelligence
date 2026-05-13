-- Databricks notebook source
-- MAGIC %md
-- MAGIC # NikePulse Gold Layer - KPI Tables
-- MAGIC
-- MAGIC This notebook creates business-ready KPI tables from Silver data using Spark SQL.

-- COMMAND ----------

CREATE DATABASE IF NOT EXISTS nikepulse_gold;

-- COMMAND ----------

USE nikepulse_gold;

-- COMMAND ----------

-- 1. Revenue by region
CREATE OR REPLACE TABLE nikepulse_gold.region_revenue AS
SELECT
    region,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(price_per_unit), 2) AS avg_price_per_unit,
    COUNT(*) AS transaction_count
FROM nikepulse_silver.sales
GROUP BY region
ORDER BY total_revenue DESC;

-- COMMAND ----------

-- 2. Revenue by retailer
CREATE OR REPLACE TABLE nikepulse_gold.retailer_revenue AS
SELECT
    retailer,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold,
    COUNT(*) AS transaction_count
FROM nikepulse_silver.sales
GROUP BY retailer
ORDER BY total_revenue DESC;

-- COMMAND ----------

-- 3. Sales method performance
CREATE OR REPLACE TABLE nikepulse_gold.sales_method_performance AS
SELECT
    sales_method,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS total_units_sold,
    COUNT(*) AS transaction_count
FROM nikepulse_silver.sales
GROUP BY sales_method
ORDER BY total_revenue DESC;

-- COMMAND ----------

-- 4. Top-selling products
CREATE OR REPLACE TABLE nikepulse_gold.top_selling_products AS
SELECT
    product_name,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(price_per_unit), 2) AS avg_price_per_unit,
    COUNT(*) AS transaction_count
FROM nikepulse_silver.sales
GROUP BY product_name
ORDER BY total_units_sold DESC;

-- COMMAND ----------

-- 5. Monthly revenue trend
CREATE OR REPLACE TABLE nikepulse_gold.monthly_revenue_trend AS
SELECT
    DATE_TRUNC('month', sale_date) AS sales_month,
    SUM(revenue) AS monthly_revenue,
    SUM(quantity) AS monthly_units_sold,
    COUNT(*) AS transaction_count
FROM nikepulse_silver.sales
GROUP BY DATE_TRUNC('month', sale_date)
ORDER BY sales_month;

-- COMMAND ----------

-- 6. Review sentiment distribution
CREATE OR REPLACE TABLE nikepulse_gold.review_sentiment_distribution AS
SELECT
    rating_group,
    COUNT(*) AS review_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM nikepulse_silver.reviews
GROUP BY rating_group
ORDER BY review_count DESC;

-- COMMAND ----------

-- 7. Average rating by product
CREATE OR REPLACE TABLE nikepulse_gold.product_review_summary AS
SELECT
    product_name,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS total_reviews,
    SUM(CASE WHEN rating_group = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN rating_group = 'neutral' THEN 1 ELSE 0 END) AS neutral_reviews,
    SUM(CASE WHEN rating_group = 'negative' THEN 1 ELSE 0 END) AS negative_reviews
FROM nikepulse_silver.reviews
GROUP BY product_name
ORDER BY total_reviews DESC;

-- COMMAND ----------

-- 8. Low-rated products needing attention
CREATE OR REPLACE TABLE nikepulse_gold.low_rated_products AS
SELECT
    product_name,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS total_reviews
FROM nikepulse_silver.reviews
GROUP BY product_name
HAVING AVG(rating) < 3.5
ORDER BY avg_rating ASC;

-- COMMAND ----------

-- 9. Product intelligence summary
CREATE OR REPLACE TABLE nikepulse_gold.product_intelligence_summary AS
SELECT
    COALESCE(s.product_name, r.product_name) AS product_name,
    SUM(s.revenue) AS total_revenue,
    SUM(s.quantity) AS total_units_sold,
    ROUND(AVG(s.price_per_unit), 2) AS avg_price_per_unit,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(DISTINCT r.review_text) AS total_reviews
FROM nikepulse_silver.sales s
FULL OUTER JOIN nikepulse_silver.reviews r
    ON LOWER(TRIM(s.product_name)) = LOWER(TRIM(r.product_name))
GROUP BY COALESCE(s.product_name, r.product_name)
ORDER BY total_revenue DESC;

-- COMMAND ----------

-- 10. Data quality summary
CREATE OR REPLACE TABLE nikepulse_gold.data_quality_summary AS
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM nikepulse_silver.products
UNION ALL
SELECT 'sales' AS table_name, COUNT(*) AS row_count FROM nikepulse_silver.sales
UNION ALL
SELECT 'reviews' AS table_name, COUNT(*) AS row_count FROM nikepulse_silver.reviews;

-- COMMAND ----------

SHOW TABLES IN nikepulse_gold;

-- COMMAND ----------

SELECT * FROM nikepulse_gold.data_quality_summary;

-- COMMAND ----------

SELECT * FROM nikepulse_gold.region_revenue;

-- COMMAND ----------

SELECT * FROM nikepulse_gold.top_selling_products LIMIT 10;

-- COMMAND ----------

SELECT * FROM nikepulse_gold.review_sentiment_distribution;