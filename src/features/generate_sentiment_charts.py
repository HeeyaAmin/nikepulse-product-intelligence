from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_sentiment_data(project_root: Path) -> pd.DataFrame:
    file_path = project_root / "data" / "processed" / "reviews_with_sentiment.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "reviews_with_sentiment.csv not found. Run sentiment_analysis.py first."
        )

    return pd.read_csv(file_path)


def save_sentiment_distribution_chart(df: pd.DataFrame, figures_dir: Path) -> None:
    sentiment_counts = df["sentiment_label"].value_counts()

    plt.figure(figsize=(8, 5))
    sentiment_counts.plot(kind="bar")
    plt.title("Nike Review Sentiment Distribution")
    plt.xlabel("Sentiment Label")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = figures_dir / "sentiment_distribution.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Saved chart: {output_path}")


def save_rating_by_sentiment_chart(df: pd.DataFrame, figures_dir: Path) -> None:
    rating_by_sentiment = (
        df.groupby("sentiment_label")["rating"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    rating_by_sentiment.plot(kind="bar")
    plt.title("Average Rating by Sentiment")
    plt.xlabel("Sentiment Label")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = figures_dir / "rating_by_sentiment.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Saved chart: {output_path}")


def save_top_positive_products_chart(df: pd.DataFrame, figures_dir: Path) -> None:
    positive_df = df[df["sentiment_label"] == "Positive"]

    top_positive_products = positive_df["title"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    top_positive_products.plot(kind="bar")
    plt.title("Top Products by Positive Reviews")
    plt.xlabel("Product")
    plt.ylabel("Positive Review Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = figures_dir / "top_positive_reviewed_products.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Saved chart: {output_path}")


def main():
    project_root = Path(__file__).resolve().parents[2]
    figures_dir = project_root / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    df = load_sentiment_data(project_root)

    save_sentiment_distribution_chart(df, figures_dir)
    save_rating_by_sentiment_chart(df, figures_dir)
    save_top_positive_products_chart(df, figures_dir)

    print("\nSentiment charts generated successfully.")


if __name__ == "__main__":
    main()
    