from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_sales_data(project_root: Path) -> pd.DataFrame:
    """
    Load cleaned Nike sales data.
    """
    sales_path = project_root / "data" / "processed" / "clean_sales.csv"

    if not sales_path.exists():
        raise FileNotFoundError(f"File not found: {sales_path}")

    return pd.read_csv(sales_path)


def prepare_features(df: pd.DataFrame):
    """
    Prepare feature matrix X and target vector y.
    Target: units_sold
    """
    required_columns = [
        "product",
        "region",
        "retailer",
        "sales_method",
        "state",
        "price_per_unit",
        "year",
        "month",
        "quarter",
        "units_sold",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    model_df = df[required_columns].copy()

    # Remove rows where target is missing
    model_df = model_df.dropna(subset=["units_sold"])

    X = model_df.drop(columns=["units_sold"])
    y = model_df["units_sold"]

    categorical_features = [
        "product",
        "region",
        "retailer",
        "sales_method",
        "state",
    ]

    numeric_features = [
        "price_per_unit",
        "year",
        "month",
        "quarter",
    ]

    return X, y, categorical_features, numeric_features


def build_preprocessor(categorical_features, numeric_features):
    """
    Build preprocessing pipeline for categorical and numeric columns.
    """
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_transformer, categorical_features),
            ("numeric", numeric_transformer, numeric_features),
        ]
    )

    return preprocessor


def build_models(preprocessor):
    """
    Create baseline and tree-based demand prediction models.
    """
    linear_regression_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", LinearRegression()),
        ]
    )

    random_forest_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=200,
                    max_depth=12,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    return {
        "Linear Regression": linear_regression_model,
        "Random Forest Regressor": random_forest_model,
    }


def evaluate_model(model, X_test, y_test):
    """
    Evaluate regression model performance.
    """
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    return {
        "mae": mae,
        "rmse": rmse,
        "r2_score": r2,
        "predictions": predictions,
    }


def save_metrics(metrics_list, project_root: Path):
    """
    Save model metrics to reports/model_metrics.csv.
    """
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_df = pd.DataFrame(metrics_list)
    output_path = reports_dir / "model_metrics.csv"
    metrics_df.to_csv(output_path, index=False)

    print(f"\nSaved model metrics: {output_path}")
    print(metrics_df)


def save_prediction_chart(y_test, predictions, project_root: Path):
    """
    Save predicted vs actual units sold chart.
    """
    figures_dir = project_root / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, predictions, alpha=0.6)
    plt.title("Predicted vs Actual Units Sold")
    plt.xlabel("Actual Units Sold")
    plt.ylabel("Predicted Units Sold")

    min_value = min(y_test.min(), predictions.min())
    max_value = max(y_test.max(), predictions.max())
    plt.plot([min_value, max_value], [min_value, max_value], linestyle="--")

    plt.tight_layout()

    output_path = figures_dir / "predicted_vs_actual_units_sold.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Saved prediction chart: {output_path}")


def save_best_model(model, project_root: Path):
    """
    Save the best trained model.
    """
    models_dir = project_root / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    output_path = models_dir / "demand_prediction_model.joblib"
    joblib.dump(model, output_path)

    print(f"Saved best model: {output_path}")


def main():
    project_root = Path(__file__).resolve().parents[2]

    sales_df = load_sales_data(project_root)

    X, y, categorical_features, numeric_features = prepare_features(sales_df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    preprocessor = build_preprocessor(categorical_features, numeric_features)
    models = build_models(preprocessor)

    metrics_list = []
    best_model = None
    best_model_name = None
    best_r2 = float("-inf")
    best_predictions = None

    print("\nTraining demand prediction models...")

    for model_name, model in models.items():
        print(f"\nTraining: {model_name}")

        model.fit(X_train, y_train)

        results = evaluate_model(model, X_test, y_test)

        metrics_list.append(
            {
                "model": model_name,
                "mae": round(results["mae"], 4),
                "rmse": round(results["rmse"], 4),
                "r2_score": round(results["r2_score"], 4),
            }
        )

        print(f"MAE: {results['mae']:.4f}")
        print(f"RMSE: {results['rmse']:.4f}")
        print(f"R2 Score: {results['r2_score']:.4f}")

        if results["r2_score"] > best_r2:
            best_r2 = results["r2_score"]
            best_model = model
            best_model_name = model_name
            best_predictions = results["predictions"]

    save_metrics(metrics_list, project_root)
    save_prediction_chart(y_test, best_predictions, project_root)
    save_best_model(best_model, project_root)

    print("\nDemand prediction completed successfully.")
    print(f"Best Model: {best_model_name}")
    print(f"Best R2 Score: {best_r2:.4f}")


if __name__ == "__main__":
    main()