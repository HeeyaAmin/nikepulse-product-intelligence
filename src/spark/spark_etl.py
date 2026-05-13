from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, regexp_replace, when, expr, coalesce

def create_spark_session():
    return (
        SparkSession.builder
        .appName("NikePulse PySpark ETL")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )


def read_csv_safely(spark, file_path):
    """
    Reads CSV files safely using options that handle messy retail/product data,
    including quoted text, commas inside descriptions, and multiline fields.
    """
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


def clean_products(products_df):
    """
    Cleans Nike product catalog data.

    Original columns include:
    index, url, name, sub_title, brand, model, color, price, currency,
    availability, description, raw_description, avg_rating, review_count,
    images, available_sizes, uniq_id, scraped_at
    """
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

        # Safe price cleaning and casting
        .withColumn("price_clean", regexp_replace(col("price").cast("string"), "[$,]", ""))
        .withColumn("price", expr("try_cast(price_clean as double)"))
        .drop("price_clean")

        # Safe numeric casting
        .withColumn("avg_rating", expr("try_cast(avg_rating as double)"))
        .withColumn("review_count", expr("try_cast(review_count as int)"))

        # Remove duplicate products
        .dropDuplicates(["product_id"])

        # Keep only useful product rows
        .dropna(subset=["product_id", "product_name"])
    )


def clean_sales(sales_df):
    """
    Cleans Nike sales transaction data.

    Original columns include:
    Invoice Date, Product, Region, Retailer, Sales Method, State,
    Price per Unit, Total Sales, Units Sold
    """
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

        # Safe numeric cleaning and casting
        .withColumn("price_per_unit_clean", regexp_replace(col("price_per_unit").cast("string"), "[$,]", ""))
        .withColumn("revenue_clean", regexp_replace(col("revenue").cast("string"), "[$,]", ""))
        .withColumn("quantity_clean", regexp_replace(col("quantity").cast("string"), "[,]", ""))

        .withColumn("price_per_unit", expr("try_cast(price_per_unit_clean as double)"))
        .withColumn("revenue", expr("try_cast(revenue_clean as double)"))
        .withColumn("quantity", expr("try_cast(quantity_clean as int)"))

        .drop("price_per_unit_clean", "revenue_clean", "quantity_clean")

        # Keep only valid sales rows
        .dropna(subset=["sale_date", "product_name", "revenue", "quantity"])
    )


def clean_reviews(reviews_df):
    """
    Cleans Nike shoe review data.

    Original columns include:
    Rating, Review Date, Location, Username, Review, Fit Feedback,
    Comfort Feedback, Recommend Feedback, title, pid
    """
    return (
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

        # Keep only useful review rows
        .dropna(subset=["review_text", "rating"])
    )


def main():
    spark = create_spark_session()

    print("Starting NikePulse PySpark ETL...")

    products_df = read_csv_safely(spark, "data/raw/nike_products.csv")
    sales_df = read_csv_safely(spark, "data/raw/nike_sales.csv")
    reviews_df = read_csv_safely(spark, "data/raw/nike_shoe_reviews.csv")

    print("Raw products columns:", products_df.columns)
    print("Raw sales columns:", sales_df.columns)
    print("Raw reviews columns:", reviews_df.columns)

    clean_products_df = clean_products(products_df)
    clean_sales_df = clean_sales(sales_df)
    clean_reviews_df = clean_reviews(reviews_df)

    print("Cleaned products count:", clean_products_df.count())
    print("Cleaned sales count:", clean_sales_df.count())
    print("Cleaned reviews count:", clean_reviews_df.count())

    clean_products_df.write.mode("overwrite").parquet("data/processed/products")
    clean_sales_df.write.mode("overwrite").parquet("data/processed/sales")
    clean_reviews_df.write.mode("overwrite").parquet("data/processed/reviews")

    print("PySpark ETL completed successfully.")
    print("Processed files saved to:")
    print("data/processed/products")
    print("data/processed/sales")
    print("data/processed/reviews")

    spark.stop()


if __name__ == "__main__":
    main()