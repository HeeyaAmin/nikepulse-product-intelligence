from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_sales_data(project_root: Path) -> pd.DataFrame:
    sales_path = project_root / "data" / "processed" / "clean_sales.csv"
    return pd.read_csv(sales_path)


def save_bar_chart(data, title, xlabel, ylabel, output_path):
    plt.figure(figsize=(10, 6))
    data.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved chart: {output_path}")


def generate_sales_charts(sales_df: pd.DataFrame, figures_dir: Path):
    revenue_by_product = (
        sales_df.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    save_bar_chart(
        revenue_by_product,
        "Revenue by Product Category",
        "Product Category",
        "Total Sales",
        figures_dir / "revenue_by_product.png",
    )

    revenue_by_region = (
        sales_df.groupby("region")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    save_bar_chart(
        revenue_by_region,
        "Revenue by Region",
        "Region",
        "Total Sales",
        figures_dir / "revenue_by_region.png",
    )

    revenue_by_method = (
        sales_df.groupby("sales_method")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    save_bar_chart(
        revenue_by_method,
        "Revenue by Sales Method",
        "Sales Method",
        "Total Sales",
        figures_dir / "revenue_by_sales_method.png",
    )

    monthly_sales = (
        sales_df.groupby(["year", "month"])["total_sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["year_month"] = (
        monthly_sales["year"].astype(str)
        + "-"
        + monthly_sales["month"].astype(str).str.zfill(2)
    )

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales["year_month"], monthly_sales["total_sales"], marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    output_path = figures_dir / "monthly_sales_trend.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved chart: {output_path}")


def main():
    project_root = Path(__file__).resolve().parents[2]
    figures_dir = project_root / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    sales_df = load_sales_data(project_root)

    generate_sales_charts(sales_df, figures_dir)

    print("\nCharts generated successfully.")


if __name__ == "__main__":
    main()