# NikePulse Databricks Workflow

This folder contains a Databricks-ready version of the NikePulse data engineering pipeline.

## Purpose

The goal of this workflow is to show how NikePulse can be executed in a cloud-scale data engineering environment using Databricks, PySpark, Spark SQL, and Delta Lake.

## Architecture

This workflow follows the Medallion Architecture:

### Bronze Layer

Raw Nike datasets are ingested from CSV files and stored as Delta tables.

Tables:

- `nikepulse_bronze.products_raw`
- `nikepulse_bronze.sales_raw`
- `nikepulse_bronze.reviews_raw`

### Silver Layer

Raw data is cleaned, standardized, and validated using PySpark transformations.

Cleaning steps include:

- Standardizing column names
- Removing duplicate product records
- Cleaning currency and numeric fields
- Handling malformed values using safe casting
- Parsing inconsistent date formats
- Creating review sentiment groups
- Removing unusable null records

Tables:

- `nikepulse_silver.products`
- `nikepulse_silver.sales`
- `nikepulse_silver.reviews`

### Gold Layer

Business-ready KPI tables are created using Spark SQL.

Gold tables include:

- `region_revenue`
- `retailer_revenue`
- `sales_method_performance`
- `top_selling_products`
- `monthly_revenue_trend`
- `review_sentiment_distribution`
- `product_review_summary`
- `low_rated_products`
- `product_intelligence_summary`
- `data_quality_summary`

## Workflow Order

Run the files in this order:

1. `01_bronze_ingestion.py`
2. `02_silver_transformations.py`
3. `03_gold_kpi_tables.sql`

## Input Data

Upload the raw datasets to Databricks under:

```text
/FileStore/nikepulse/raw/