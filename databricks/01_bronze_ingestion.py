# Databricks notebook source
# MAGIC %md
# MAGIC # NikePulse Bronze Layer - Raw Data Ingestion
# MAGIC
# MAGIC This notebook ingests raw Nike product, sales, and review CSV files into Bronze Delta tables.

# COMMAND ----------

from pyspark.sql import SparkSession

# COMMAND ----------

# Create database/schema for Bronze layer
spark.sql("CREATE DATABASE IF NOT EXISTS nikepulse_bronze")

# COMMAND ----------

# File paths
# In Databricks, upload your raw CSV files to DBFS/FileStore or cloud storage.
# Example DBFS paths:
products_path = "/FileStore/nikepulse/raw/nike_products.csv"
sales_path = "/FileStore/nikepulse/raw/nike_sales.csv"
reviews_path = "/FileStore/nikepulse/raw/nike_shoe_reviews.csv"

# COMMAND ----------

def read_csv_safely(file_path):
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .option("multiLine", True)
        .option("quote", '"')
        .option("escape", '"')
        .option("mode", "PERMISSIVE")
        .csv(file_path)
    )

# COMMAND ----------

products_raw = read_csv_safely(products_path)
sales_raw = read_csv_safely(sales_path)
reviews_raw = read_csv_safely(reviews_path)

# COMMAND ----------

print("Products columns:", products_raw.columns)
print("Sales columns:", sales_raw.columns)
print("Reviews columns:", reviews_raw.columns)

# COMMAND ----------

display(products_raw.limit(5))
display(sales_raw.limit(5))
display(reviews_raw.limit(5))

# COMMAND ----------

# Save raw data as Bronze Delta tables
products_raw.write.mode("overwrite").format("delta").saveAsTable("nikepulse_bronze.products_raw")
sales_raw.write.mode("overwrite").format("delta").saveAsTable("nikepulse_bronze.sales_raw")
reviews_raw.write.mode("overwrite").format("delta").saveAsTable("nikepulse_bronze.reviews_raw")

# COMMAND ----------

print("Bronze ingestion completed successfully.")

# COMMAND ----------

spark.sql("SHOW TABLES IN nikepulse_bronze").show()