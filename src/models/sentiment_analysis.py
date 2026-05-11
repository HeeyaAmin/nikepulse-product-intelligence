from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def load_reviews(project_root: Path) -> pd.DataFrame:
    reviews_path = project_root / "data" / "processed" / "clean_reviews.csv"

    if not reviews_path.exists():
        raise FileNotFoundError(f"File not found: {reviews_path}")

    return pd.read_csv(reviews_path)


def get_sentiment_label(score: float) -> str:
    """
    Convert VADER compound score into sentiment label.
    """
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def add_sentiment_scores(reviews_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add sentiment score and sentiment label to review dataset.
    """
    df = reviews_df.copy()

    analyzer = SentimentIntensityAnalyzer()

    df["review"] = df["review"].fillna("").astype(str)

    df["sentiment_score"] = df["review"].apply(
        lambda text: analyzer.polarity_scores(text)["compound"]
    )

    df["sentiment_label"] = df["sentiment_score"].apply(get_sentiment_label)

    return df


def summarize_sentiment(df: pd.DataFrame) -> None:
    print("\n" + "=" * 70)
    print("NIKE REVIEW SENTIMENT SUMMARY")
    print("=" * 70)

    print("\nSentiment Label Distribution:")
    print(df["sentiment_label"].value_counts())

    print("\nAverage Sentiment Score:")
    print(round(df["sentiment_score"].mean(), 4))

    print("\nAverage Rating by Sentiment:")
    print(df.groupby("sentiment_label")["rating"].mean().sort_values(ascending=False))

    print("\nTop Products by Positive Review Count:")
    positive_reviews = df[df["sentiment_label"] == "Positive"]
    print(positive_reviews["title"].value_counts().head(10))

    print("\nTop Products by Negative Review Count:")
    negative_reviews = df[df["sentiment_label"] == "Negative"]
    print(negative_reviews["title"].value_counts().head(10))


def save_sentiment_data(df: pd.DataFrame, project_root: Path) -> None:
    output_path = project_root / "data" / "processed" / "reviews_with_sentiment.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved sentiment dataset: {output_path}")


def main():
    project_root = Path(__file__).resolve().parents[2]

    reviews_df = load_reviews(project_root)
    sentiment_df = add_sentiment_scores(reviews_df)

    summarize_sentiment(sentiment_df)
    save_sentiment_data(sentiment_df, project_root)

    print("\nSentiment analysis completed successfully.")


if __name__ == "__main__":
    main()
    