# Databricks notebook source
# MAGIC %md
# MAGIC # NikePulse Silver Layer - PySpark Transformations
# MAGIC
# MAGIC This notebook cleans and standardizes raw Nike product, sales, and review data from Bronze tables.

# COMMAND ----------

from pyspark.sql.functions import col, lower, trim, regexp_replace, when, expr, coalesce

# COMMAND ----------

spark.sql("CREATE DATABASE IF NOT EXISTS nikepulse_silver")

# COMMAND ----------

products_df = spark.table("nikepulse_bronze.products_raw")
sales_df = spark.table("nikepulse_bronze.sales_raw")
reviews_df = spark.table("nikepulse_bronze.reviews_raw")

# COMMAND ----------

def clean_products(products_df):
    return (
        products_df
        .withColumnRenamed("uniq_id", "product_id")
        .withColumnRenamed("name", "product_name")
        .withColumnRenamed("sub_title", "product_subtitle")
        .withColumn("product_name", trim(col("product_name")))
        .withColumn("product_subtitle", trim(col("product_subtitle")))
        .withColumn("brand", lower(trim(col("brand"))))
        .withColumn("model", trim(col("model")))
        .withColumn("color", lower(trim(col("color"))))
        .withColumn("availability", trim(col("availability")))
        .withColumn("currency", trim(col("currency")))
        .withColumn("description", trim(col("description")))
        .withColumn("raw_description", trim(col("raw_description")))
        .withColumn("available_sizes", trim(col("available_sizes")))
        .withColumn("price_clean", regexp_replace(col("price").cast("string"), "[$,]", ""))
        .withColumn("price", expr("try_cast(price_clean as double)"))
        .drop("price_clean")
        .withColumn("avg_rating", expr("try_cast(avg_rating as double)"))
        .withColumn("review_count", expr("try_cast(review_count as int)"))
        .dropDuplicates(["product_id"])
        .dropna(subset=["product_id", "product_name"])
    )

# COMMAND ----------

def clean_sales(sales_df):
    return (
        sales_df
        .withColumnRenamed("Invoice Date", "sale_date")
        .withColumnRenamed("Product", "product_name")
        .withColumnRenamed("Region", "region")
        .withColumnRenamed("Retailer", "retailer")
        .withColumnRenamed("Sales Method", "sales_method")
        .withColumnRenamed("State", "state")
        .withColumnRenamed("Price per Unit", "price_per_unit")
        .withColumnRenamed("Total Sales", "revenue")
        .withColumnRenamed("Units Sold", "quantity")
        .withColumn(
            "sale_date",
            coalesce(
                expr("try_to_date(sale_date, 'dd-MM-yyyy')"),
                expr("try_to_date(sale_date, 'MM-dd-yyyy')"),
                expr("try_to_date(sale_date, 'yyyy-MM-dd')"),
                expr("try_to_date(sale_date, 'MM/dd/yyyy')"),
                expr("try_to_date(sale_date, 'dd/MM/yyyy')")
            )
        )
        .withColumn("product_name", trim(col("product_name")))
        .withColumn("region", trim(col("region")))
        .withColumn("retailer", trim(col("retailer")))
        .withColumn("sales_method", trim(col("sales_method")))
        .withColumn("state", trim(col("state")))
        .withColumn("price_per_unit_clean", regexp_replace(col("price_per_unit").cast("string"), "[$,]", ""))
        .withColumn("revenue_clean", regexp_replace(col("revenue").cast("string"), "[$,]", ""))
        .withColumn("quantity_clean", regexp_replace(col("quantity").cast("string"), "[,]", ""))
        .withColumn("price_per_unit", expr("try_cast(price_per_unit_clean as double)"))
        .withColumn("revenue", expr("try_cast(revenue_clean as double)"))
        .withColumn("quantity", expr("try_cast(quantity_clean as int)"))
        .drop("price_per_unit_clean", "revenue_clean", "quantity_clean")
        .dropna(subset=["sale_date", "product_name", "revenue", "quantity"])
    )

# COMMAND ----------

def clean_reviews(reviews_df):
    cleaned = (
        reviews_df
        .withColumnRenamed("pid", "product_id")
        .withColumnRenamed("Review", "review_text")
        .withColumnRenamed("Rating", "rating")
        .withColumnRenamed("Review Date", "review_date")
        .withColumnRenamed("Username", "username")
        .withColumnRenamed("Location", "location")
        .withColumnRenamed("Fit Feedback", "fit_feedback")
        .withColumnRenamed("Comfort Feedback", "comfort_feedback")
        .withColumnRenamed("Recommend Feedback", "recommend_feedback")
        .withColumnRenamed("title", "product_name")
        .withColumn("review_text", trim(col("review_text")))
        .withColumn("product_name", trim(col("product_name")))
        .withColumn("username", trim(col("username")))
        .withColumn("location", trim(col("location")))
        .withColumn("fit_feedback", trim(col("fit_feedback")))
        .withColumn("comfort_feedback", trim(col("comfort_feedback")))
        .withColumn("recommend_feedback", trim(col("recommend_feedback")))
        .withColumn("rating", expr("try_cast(rating as double)"))
        .withColumn(
            "review_date",
            coalesce(
                expr("try_to_date(review_date, 'dd-MM-yyyy')"),
                expr("try_to_date(review_date, 'MM-dd-yyyy')"),
                expr("try_to_date(review_date, 'yyyy-MM-dd')"),
                expr("try_to_date(review_date, 'MM/dd/yyyy')"),
                expr("try_to_date(review_date, 'dd/MM/yyyy')")
            )
        )
        .withColumn(
            "rating_group",
            when(col("rating") >= 4, "positive")
            .when(col("rating") == 3, "neutral")
            .otherwise("negative")
        )
        .dropna(subset=["review_text", "rating"])
    )

    if "_c0" in cleaned.columns:
        cleaned = cleaned.drop("_c0")

    return cleaned

# COMMAND ----------

products_clean = clean_products(products_df)
sales_clean = clean_sales(sales_df)
reviews_clean = clean_reviews(reviews_df)

# COMMAND ----------

print("Cleaned products count:", products_clean.count())
print("Cleaned sales count:", sales_clean.count())
print("Cleaned reviews count:", reviews_clean.count())

# COMMAND ----------

display(products_clean.limit(5))
display(sales_clean.limit(5))
display(reviews_clean.limit(5))

# COMMAND ----------

products_clean.write.mode("overwrite").format("delta").saveAsTable("nikepulse_silver.products")
sales_clean.write.mode("overwrite").format("delta").saveAsTable("nikepulse_silver.sales")
reviews_clean.write.mode("overwrite").format("delta").saveAsTable("nikepulse_silver.reviews")

# COMMAND ----------

print("Silver transformations completed successfully.")

# COMMAND ----------

spark.sql("SHOW TABLES IN nikepulse_silver").show()