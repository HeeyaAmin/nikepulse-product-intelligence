from pathlib import Path
import pandas as pd


def load_cleaned_data(project_root: Path):
    processed_dir = project_root / "data" / "processed"

    sales_df = pd.read_csv(processed_dir / "clean_sales.csv")
    products_df = pd.read_csv(processed_dir / "clean_products.csv")
    reviews_df = pd.read_csv(processed_dir / "clean_reviews.csv")

    return sales_df, products_df, reviews_df


def sales_summary(sales_df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("SALES SUMMARY")
    print("=" * 70)

    total_revenue = sales_df["total_sales"].sum()
    total_units = sales_df["units_sold"].sum()
    avg_price = sales_df["price_per_unit"].mean()

    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Units Sold: {total_units:,}")
    print(f"Average Price per Unit: ${avg_price:,.2f}")

    print("\nTop Products by Revenue:")
    print(
        sales_df.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nRevenue by Region:")
    print(
        sales_df.groupby("region")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nRevenue by Sales Method:")
    print(
        sales_df.groupby("sales_method")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )


def product_summary(products_df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("PRODUCT CATALOG SUMMARY")
    print("=" * 70)

    print(f"Total Products: {len(products_df)}")

    print("\nAverage Price:")
    print(products_df["price"].mean())

    print("\nMost Common Product Subtitles/Categories:")
    print(products_df["sub_title"].value_counts().head(10))

    print("\nAvailability Count:")
    print(products_df["availability"].value_counts())


def review_summary(reviews_df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("REVIEW SUMMARY")
    print("=" * 70)

    print(f"Total Reviews: {len(reviews_df)}")
    print(f"Average Rating: {reviews_df['rating'].mean():.2f}")

    print("\nRating Distribution:")
    print(reviews_df["rating"].value_counts().sort_index())

    print("\nTop Reviewed Products:")
    print(reviews_df["title"].value_counts().head(10))

    print("\nReview Label Distribution:")
    print(reviews_df["label"].value_counts())


def main():
    project_root = Path(__file__).resolve().parents[2]

    sales_df, products_df, reviews_df = load_cleaned_data(project_root)

    sales_summary(sales_df)
    product_summary(products_df)
    review_summary(reviews_df)

    print("\nEDA summary completed successfully.")


if __name__ == "__main__":
    main()