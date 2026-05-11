from pathlib import Path
import pandas as pd


def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file and return a pandas DataFrame.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def basic_summary(df: pd.DataFrame, dataset_name: str) -> None:
    """
    Print basic information about a dataset.
    """
    print("\n" + "=" * 60)
    print(f"{dataset_name} Dataset Summary")
    print("=" * 60)

    print(f"Shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())


def main():
    project_root = Path(__file__).resolve().parents[2]

    products_path = project_root / "data" / "raw" / "nike_products.csv"
    sales_path = project_root / "data" / "raw" / "nike_sales.csv"
    reviews_path = project_root / "data" / "raw" / "nike_shoe_reviews.csv"

    products_df = load_csv(products_path)
    sales_df = load_csv(sales_path)
    reviews_df = load_csv(reviews_path)

    basic_summary(products_df, "Nike Products")
    basic_summary(sales_df, "Nike Sales")
    basic_summary(reviews_df, "Nike Shoe Reviews")


if __name__ == "__main__":
    main()  