from pathlib import Path
import pandas as pd
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to lowercase snake_case.
    Example: 'Invoice Date' -> 'invoice_date'
    """
    df = df.copy()
    df.columns = [
        re.sub(r"[^a-zA-Z0-9]+", "_", col.strip().lower()).strip("_")
        for col in df.columns
    ]
    return df


def clean_products(products_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Nike product catalog dataset.
    """
    df = clean_column_names(products_df)

    # Drop unnecessary index-like column if present
    columns_to_drop = ["index"]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    # Handle missing values
    df["color"] = df["color"].fillna("Unknown")
    df["availability"] = df["availability"].fillna("Unknown")
    df["avg_rating"] = df["avg_rating"].fillna(0)
    df["review_count"] = df["review_count"].fillna(0)
    df["available_sizes"] = df["available_sizes"].fillna("Not Available")
    df["images"] = df["images"].fillna("Not Available")

    # Standardize data types
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce").fillna(0)
    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce").fillna(0).astype(int)

    # Create product_id from uniq_id
    if "uniq_id" in df.columns:
        df = df.rename(columns={"uniq_id": "product_id"})

    return df


def clean_sales(sales_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Nike sales transaction dataset.
    """
    df = clean_column_names(sales_df)

    # Convert date
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%d-%m-%Y", errors="coerce")

    # Convert numeric columns
    numeric_columns = ["price_per_unit", "total_sales", "units_sold"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Add useful date features
    df["year"] = df["invoice_date"].dt.year
    df["month"] = df["invoice_date"].dt.month
    df["month_name"] = df["invoice_date"].dt.month_name()
    df["quarter"] = df["invoice_date"].dt.quarter

    # Add calculated metrics
    df["revenue_per_unit_check"] = df["total_sales"] / df["units_sold"]

    return df


def clean_reviews(reviews_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Nike shoe reviews dataset.
    """
    df = clean_column_names(reviews_df)

    # Drop unnecessary index column
    if "unnamed_0" in df.columns:
        df = df.drop(columns=["unnamed_0"])

    # Keep useful columns only
    useful_columns = [
        "rating",
        "review_date",
        "location",
        "username",
        "review",
        "title",
        "subtitle",
        "colordescription",
        "fullprice",
        "discounted",
        "employeeprice",
        "currentprice",
        "islaunch",
        "pid",
        "label",
    ]

    df = df[[col for col in useful_columns if col in df.columns]]

    # Remove rows where review text or rating is missing
    df = df.dropna(subset=["review", "rating"])

    # Handle location
    df["location"] = df["location"].fillna("Unknown")

    # Convert dates
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

    # Convert numeric columns
    numeric_columns = ["rating", "fullprice", "employeeprice", "currentprice"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rename columns for readability
    df = df.rename(
        columns={
            "colordescription": "color_description",
            "fullprice": "full_price",
            "employeeprice": "employee_price",
            "currentprice": "current_price",
            "islaunch": "is_launch",
            "pid": "product_review_id",
        }
    )

    # Add review year/month
    df["review_year"] = df["review_date"].dt.year
    df["review_month"] = df["review_date"].dt.month

    return df


def save_cleaned_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save cleaned DataFrame to CSV.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def main():
    project_root = Path(__file__).resolve().parents[2]

    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"

    products_path = raw_dir / "nike_products.csv"
    sales_path = raw_dir / "nike_sales.csv"
    reviews_path = raw_dir / "nike_shoe_reviews.csv"

    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)
    reviews_df = pd.read_csv(reviews_path)

    clean_products_df = clean_products(products_df)
    clean_sales_df = clean_sales(sales_df)
    clean_reviews_df = clean_reviews(reviews_df)

    save_cleaned_data(clean_products_df, processed_dir / "clean_products.csv")
    save_cleaned_data(clean_sales_df, processed_dir / "clean_sales.csv")
    save_cleaned_data(clean_reviews_df, processed_dir / "clean_reviews.csv")

    print("\nCleaning completed successfully.")
    print("Clean Products Shape:", clean_products_df.shape)
    print("Clean Sales Shape:", clean_sales_df.shape)
    print("Clean Reviews Shape:", clean_reviews_df.shape)


if __name__ == "__main__":
    main()