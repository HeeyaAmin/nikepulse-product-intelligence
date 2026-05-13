from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# Page Config
# ============================================================
st.set_page_config(
    page_title="NikePulse Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Custom Nike-Inspired CSS
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f7f7;
        color: #111111;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }

    section[data-testid="stSidebar"] {
        background-color: #111111;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #1f1f1f;
        border-color: #444444;
    }

    .hero-card {
        background: linear-gradient(135deg, #111111 0%, #2b2b2b 100%);
        padding: 2.4rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #d4d4d4;
        max-width: 900px;
        line-height: 1.6;
    }

    .hero-tag {
        display: inline-block;
        background-color: #ffffff;
        color: #111111;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.8px;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 900;
        color: #111111;
        margin-top: 1.2rem;
        margin-bottom: 0.45rem;
        letter-spacing: -0.5px;
    }

    .section-caption {
        color: #555555;
        font-size: 0.98rem;
        margin-bottom: 1.2rem;
        line-height: 1.5;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 700;
        color: #555555;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 900;
        color: #111111;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }

    div[data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
    }

    div[data-testid="stImage"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }

    hr {
        border: none;
        border-top: 1px solid #dddddd;
        margin: 1.5rem 0;
    }

    .insight-card {
        background-color: #ffffff;
        padding: 1.1rem 1.2rem;
        border-radius: 18px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    .insight-title {
        font-size: 0.85rem;
        font-weight: 800;
        color: #555555;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.4rem;
    }

    .insight-value {
        font-size: 1.2rem;
        font-weight: 900;
        color: #111111;
    }

    .pipeline-card {
        background-color: #ffffff;
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    .pipeline-step {
        font-size: 1.05rem;
        font-weight: 800;
        color: #111111;
        margin-bottom: 0.35rem;
    }

    .pipeline-desc {
        font-size: 0.95rem;
        color: #555555;
        line-height: 1.5;
    }

    .footer {
        text-align: center;
        color: #777777;
        font-size: 0.9rem;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Data Loading
# ============================================================
@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[1]

    products_parquet_path = project_root / "data" / "processed" / "products"
    sales_parquet_path = project_root / "data" / "processed" / "sales"
    reviews_parquet_path = project_root / "data" / "processed" / "reviews"

    missing_paths = []

    if not products_parquet_path.exists():
        missing_paths.append(str(products_parquet_path))

    if not sales_parquet_path.exists():
        missing_paths.append(str(sales_parquet_path))

    if not reviews_parquet_path.exists():
        missing_paths.append(str(reviews_parquet_path))

    if missing_paths:
        st.error("Processed PySpark Parquet files are missing.")
        st.markdown(
            """
            Please run the PySpark ETL pipeline first:

            ```bash
            python src/spark/spark_etl.py
            ```
            """
        )
        st.write("Missing paths:")
        st.write(missing_paths)
        st.stop()

    try:
        products_df = pd.read_parquet(products_parquet_path)
        sales_df = pd.read_parquet(sales_parquet_path)
        reviews_df = pd.read_parquet(reviews_parquet_path)
    except Exception as error:
        st.error("Unable to read Parquet files.")
        st.markdown(
            """
            Make sure `pyarrow` is installed:

            ```bash
            pip install pyarrow
            ```
            """
        )
        st.exception(error)
        st.stop()

    return sales_df, reviews_df, products_df, project_root


sales_df, reviews_df, products_df, project_root = load_data()


# ============================================================
# Data Compatibility Layer
# ============================================================
def prepare_dashboard_data(sales_df, reviews_df, products_df):
    sales_df = sales_df.copy()
    reviews_df = reviews_df.copy()
    products_df = products_df.copy()

    # Standardize sales columns for dashboard compatibility
    if "product" not in sales_df.columns and "product_name" in sales_df.columns:
        sales_df["product"] = sales_df["product_name"]

    if "total_sales" not in sales_df.columns and "revenue" in sales_df.columns:
        sales_df["total_sales"] = sales_df["revenue"]

    if "units_sold" not in sales_df.columns and "quantity" in sales_df.columns:
        sales_df["units_sold"] = sales_df["quantity"]

    if "sale_date" in sales_df.columns:
        sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], errors="coerce")

        if "year" not in sales_df.columns:
            sales_df["year"] = sales_df["sale_date"].dt.year

        if "month" not in sales_df.columns:
            sales_df["month"] = sales_df["sale_date"].dt.month

        if "quarter" not in sales_df.columns:
            sales_df["quarter"] = sales_df["sale_date"].dt.quarter

    # Standardize reviews columns for dashboard compatibility
    if "title" not in reviews_df.columns and "product_name" in reviews_df.columns:
        reviews_df["title"] = reviews_df["product_name"]

    if "review" not in reviews_df.columns and "review_text" in reviews_df.columns:
        reviews_df["review"] = reviews_df["review_text"]

    if "sentiment_label" not in reviews_df.columns:
        if "rating_group" in reviews_df.columns:
            sentiment_map = {
                "positive": "Positive",
                "neutral": "Neutral",
                "negative": "Negative",
            }
            reviews_df["sentiment_label"] = reviews_df["rating_group"].map(sentiment_map)
        elif "rating" in reviews_df.columns:
            reviews_df["sentiment_label"] = reviews_df["rating"].apply(
                lambda rating: "Positive"
                if rating >= 4
                else ("Neutral" if rating == 3 else "Negative")
            )
        else:
            reviews_df["sentiment_label"] = "Unknown"

    if "sentiment_score" not in reviews_df.columns:
        if "rating" in reviews_df.columns:
            reviews_df["sentiment_score"] = reviews_df["rating"] / 5
        else:
            reviews_df["sentiment_score"] = None

    if "review_date" in reviews_df.columns:
        reviews_df["review_date"] = pd.to_datetime(reviews_df["review_date"], errors="coerce")

    # Ensure numeric columns are numeric
    for col_name in ["total_sales", "units_sold", "price_per_unit"]:
        if col_name in sales_df.columns:
            sales_df[col_name] = pd.to_numeric(sales_df[col_name], errors="coerce")

    if "rating" in reviews_df.columns:
        reviews_df["rating"] = pd.to_numeric(reviews_df["rating"], errors="coerce")

    if "price" in products_df.columns:
        products_df["price"] = pd.to_numeric(products_df["price"], errors="coerce")

    return sales_df, reviews_df, products_df


sales_df, reviews_df, products_df = prepare_dashboard_data(
    sales_df,
    reviews_df,
    products_df,
)


# ============================================================
# Helper Functions
# ============================================================
def apply_nike_theme(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            size=14,
            color="#111111",
        ),
        title=dict(
            font=dict(size=20, color="#111111"),
            x=0.02,
        ),
        margin=dict(l=30, r=30, t=70, b=40),
        hoverlabel=dict(
            bgcolor="#111111",
            font_size=13,
            font_color="white",
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#dddddd",
        tickfont=dict(color="#333333"),
    )

    fig.update_yaxes(
        gridcolor="#eeeeee",
        linecolor="#dddddd",
        tickfont=dict(color="#333333"),
    )

    return fig


def section_header(title: str, caption: str):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="section-caption">{caption}</div>',
        unsafe_allow_html=True,
    )


def format_currency(value):
    if pd.isna(value):
        return "$0"
    return f"${value:,.0f}"


def safe_unique_values(df, column_name):
    if column_name not in df.columns:
        return []

    values = df[column_name].dropna().unique().tolist()
    return sorted(values)


def safe_metric_value(value, fallback=0):
    if pd.isna(value):
        return fallback
    return value


# ============================================================
# Hero Section
# ============================================================
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-tag">Data engineering + product intelligence platform</div>
        <div class="hero-title">NikePulse</div>
        <div class="hero-subtitle">
            A Nike-inspired product intelligence platform powered by PySpark ETL, SQL KPI logic,
            Databricks-style medallion architecture, customer sentiment analysis, demand prediction,
            and Streamlit dashboards.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================
st.sidebar.markdown("## 👟 NikePulse")
st.sidebar.markdown("**Product Intelligence Hub**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Sales Performance",
        "Regional Insights",
        "Customer Sentiment",
        "Demand Prediction",
        "Data Engineering Pipeline",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Control Room")

region_options = safe_unique_values(sales_df, "region")
product_options = safe_unique_values(sales_df, "product")
sales_method_options = safe_unique_values(sales_df, "sales_method")

selected_region = st.sidebar.multiselect(
    "Region",
    options=region_options,
    default=region_options,
)

selected_product = st.sidebar.multiselect(
    "Product",
    options=product_options,
    default=product_options,
)

selected_sales_method = st.sidebar.multiselect(
    "Sales Method",
    options=sales_method_options,
    default=sales_method_options,
)

filtered_sales = sales_df.copy()

if region_options:
    filtered_sales = filtered_sales[filtered_sales["region"].isin(selected_region)]

if product_options:
    filtered_sales = filtered_sales[filtered_sales["product"].isin(selected_product)]

if sales_method_options:
    filtered_sales = filtered_sales[filtered_sales["sales_method"].isin(selected_sales_method)]

if filtered_sales.empty and page != "Data Engineering Pipeline":
    st.warning("No data available for the selected filters. Please adjust the sidebar filters.")
    st.stop()


# ============================================================
# Page 1: Executive Overview
# ============================================================
if page == "Executive Overview":
    section_header(
        "Executive Overview",
        "High-level business snapshot across sales, demand, pricing, and customer signals.",
    )

    total_revenue = filtered_sales["total_sales"].sum()
    total_units = filtered_sales["units_sold"].sum()
    avg_price = filtered_sales["price_per_unit"].mean()
    avg_rating = reviews_df["rating"].mean() if "rating" in reviews_df.columns else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", format_currency(total_revenue))
    col2.metric("Units Sold", f"{safe_metric_value(total_units):,.0f}")
    col3.metric("Avg. Price / Unit", f"${safe_metric_value(avg_price):,.2f}")
    col4.metric("Avg. Review Rating", f"{safe_metric_value(avg_rating):.2f}/5")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        monthly_sales = (
            filtered_sales.dropna(subset=["year", "month"])
            .groupby(["year", "month"])["total_sales"]
            .sum()
            .reset_index()
        )

        if not monthly_sales.empty:
            monthly_sales["year_month"] = (
                monthly_sales["year"].astype(int).astype(str)
                + "-"
                + monthly_sales["month"].astype(int).astype(str).str.zfill(2)
            )

            fig = px.line(
                monthly_sales,
                x="year_month",
                y="total_sales",
                markers=True,
                title="Monthly Sales Trend",
            )
            fig = apply_nike_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Monthly sales trend is unavailable because sale dates are missing.")

    with col_right:
        top_region = (
            filtered_sales.groupby("region")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        top_product = (
            filtered_sales.groupby("product")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        top_method = (
            filtered_sales.groupby("sales_method")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        top_region_value = top_region.index[0] if not top_region.empty else "N/A"
        top_product_value = top_product.index[0] if not top_product.empty else "N/A"
        top_method_value = top_method.index[0] if not top_method.empty else "N/A"

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">Top Region</div>
                <div class="insight-value">{top_region_value}</div>
            </div>
            <div class="insight-card">
                <div class="insight-title">Top Product Category</div>
                <div class="insight-value">{top_product_value}</div>
            </div>
            <div class="insight-card">
                <div class="insight-title">Top Sales Method</div>
                <div class="insight-value">{top_method_value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Top Products by Revenue</div>', unsafe_allow_html=True)

    product_revenue = (
        filtered_sales.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        product_revenue,
        x="product",
        y="total_sales",
        title="Revenue by Product Category",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# Page 2: Sales Performance
# ============================================================
elif page == "Sales Performance":
    section_header(
        "Sales & Product Performance",
        "Analyze product categories, revenue contribution, unit movement, and price-demand behavior.",
    )

    col1, col2 = st.columns(2)

    with col1:
        revenue_by_product = (
            filtered_sales.groupby("product")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            revenue_by_product,
            x="product",
            y="total_sales",
            title="Revenue by Product",
        )
        fig = apply_nike_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        units_by_product = (
            filtered_sales.groupby("product")["units_sold"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            units_by_product,
            x="product",
            y="units_sold",
            title="Units Sold by Product",
        )
        fig = apply_nike_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Price vs Demand Behavior</div>', unsafe_allow_html=True)

    fig = px.scatter(
        filtered_sales,
        x="price_per_unit",
        y="units_sold",
        color="product",
        size="total_sales",
        hover_data=["region", "retailer", "sales_method", "state"],
        title="Price per Unit vs Units Sold",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Retailer Performance</div>', unsafe_allow_html=True)

    retailer_sales = (
        filtered_sales.groupby("retailer")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        retailer_sales,
        x="retailer",
        y="total_sales",
        title="Revenue by Retailer",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# Page 3: Regional Insights
# ============================================================
elif page == "Regional Insights":
    section_header(
        "Regional Market Insights",
        "Understand how product demand shifts across regions, states, and sales channels.",
    )

    revenue_by_region = (
        filtered_sales.groupby("region")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        revenue_by_region,
        x="region",
        y="total_sales",
        title="Revenue by Region",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        revenue_by_state = (
            filtered_sales.groupby("state")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            revenue_by_state,
            x="state",
            y="total_sales",
            title="Top 15 States by Revenue",
        )
        fig = apply_nike_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        units_by_state = (
            filtered_sales.groupby("state")["units_sold"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            units_by_state,
            x="state",
            y="units_sold",
            title="Top 15 States by Units Sold",
        )
        fig = apply_nike_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    sales_method_region = (
        filtered_sales.groupby(["region", "sales_method"])["total_sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_method_region,
        x="region",
        y="total_sales",
        color="sales_method",
        barmode="group",
        title="Sales Method Performance by Region",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# Page 4: Customer Sentiment
# ============================================================
elif page == "Customer Sentiment":
    section_header(
        "Customer Sentiment Analysis",
        "Explore review sentiment, customer satisfaction patterns, and product-level consumer response.",
    )

    col1, col2, col3 = st.columns(3)

    total_reviews = len(reviews_df)
    positive_reviews = reviews_df[reviews_df["sentiment_label"] == "Positive"]
    negative_reviews = reviews_df[reviews_df["sentiment_label"] == "Negative"]

    positive_rate = len(positive_reviews) / total_reviews * 100 if total_reviews > 0 else 0
    negative_rate = len(negative_reviews) / total_reviews * 100 if total_reviews > 0 else 0

    col1.metric("Total Reviews", f"{total_reviews:,.0f}")
    col2.metric("Positive Review Rate", f"{positive_rate:.1f}%")
    col3.metric("Negative Review Rate", f"{negative_rate:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        sentiment_counts = reviews_df["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["sentiment_label", "count"]

        fig = px.bar(
            sentiment_counts,
            x="sentiment_label",
            y="count",
            title="Review Sentiment Distribution",
        )
        fig = apply_nike_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        rating_distribution = reviews_df["rating"].value_counts().sort_index().reset_index()
        rating_distribution.columns = ["rating", "count"]

        fig = px.bar(
            rating_distribution,
            x="rating",
            y="count",
            title="Rating Distribution",
        )
        fig = apply_nike_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    rating_by_sentiment = (
        reviews_df.groupby("sentiment_label")["rating"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        rating_by_sentiment,
        x="sentiment_label",
        y="rating",
        title="Average Rating by Sentiment",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Top Products by Positive Reviews</div>', unsafe_allow_html=True)

    top_positive_products = (
        positive_reviews["title"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_positive_products.columns = ["product", "positive_review_count"]

    fig = px.bar(
        top_positive_products,
        x="product",
        y="positive_review_count",
        title="Top Products by Positive Review Count",
    )
    fig = apply_nike_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Sample Customer Reviews</div>', unsafe_allow_html=True)

    sample_cols = ["title", "rating", "sentiment_label", "sentiment_score", "review"]
    existing_cols = [col for col in sample_cols if col in reviews_df.columns]

    st.dataframe(
        reviews_df[existing_cols].head(20),
        use_container_width=True,
    )


# ============================================================
# Page 5: Demand Prediction
# ============================================================
elif page == "Demand Prediction":
    section_header(
        "Demand Prediction Model",
        "Machine learning layer for forecasting product unit demand using pricing, region, channel, and seasonal features.",
    )

    st.markdown(
        """
        The model predicts **units sold** using product category, region, retailer,
        sales method, state, price per unit, and seasonal features.
        """
    )

    metrics_path = project_root / "reports" / "model_metrics.csv"
    prediction_chart_path = (
        project_root / "reports" / "figures" / "predicted_vs_actual_units_sold.png"
    )

    if metrics_path.exists():
        metrics_df = pd.read_csv(metrics_path)

        st.markdown('<div class="section-title">Model Performance</div>', unsafe_allow_html=True)
        st.dataframe(metrics_df, use_container_width=True)

        if "r2_score" in metrics_df.columns:
            best_model_row = metrics_df.sort_values("r2_score", ascending=False).iloc[0]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Best Model", str(best_model_row["model"]))
            col2.metric("MAE", f"{best_model_row['mae']:.2f}")
            col3.metric("RMSE", f"{best_model_row['rmse']:.2f}")
            col4.metric("R² Score", f"{best_model_row['r2_score']:.3f}")
    else:
        st.warning("Model metrics file not found. Run this command first:")
        st.code("python src/models/demand_prediction.py")

    if prediction_chart_path.exists():
        st.markdown('<div class="section-title">Predicted vs Actual Units Sold</div>', unsafe_allow_html=True)
        st.image(str(prediction_chart_path), use_container_width=True)
    else:
        st.warning("Prediction chart not found. Run this command first:")
        st.code("python src/models/demand_prediction.py")

    st.markdown('<div class="section-title">Model Features</div>', unsafe_allow_html=True)

    st.markdown(
        """
        **Features used:**

        - Product category / product name
        - Region
        - Retailer
        - Sales method
        - State
        - Price per unit
        - Year
        - Month
        - Quarter
        """
    )


# ============================================================
# Page 6: Data Engineering Pipeline
# ============================================================
elif page == "Data Engineering Pipeline":
    section_header(
        "Data Engineering Pipeline",
        "Overview of the PySpark, SQL, and Databricks-style workflow powering NikePulse.",
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Products Processed", f"{len(products_df):,.0f}")
    col2.metric("Sales Records Processed", f"{len(sales_df):,.0f}")
    col3.metric("Reviews Processed", f"{len(reviews_df):,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="pipeline-card">
            <div class="pipeline-step">1. Raw Data Ingestion</div>
            <div class="pipeline-desc">
                Raw Nike product, sales, and shoe review CSV files are stored under <b>data/raw/</b>.
            </div>
        </div>

        <div class="pipeline-card">
            <div class="pipeline-step">2. PySpark ETL Processing</div>
            <div class="pipeline-desc">
                The <b>src/spark/spark_etl.py</b> pipeline standardizes schemas, cleans malformed values,
                parses inconsistent dates, safely casts numeric fields, removes duplicates, and writes
                analytics-ready Parquet outputs.
            </div>
        </div>

        <div class="pipeline-card">
            <div class="pipeline-step">3. Processed Parquet Layer</div>
            <div class="pipeline-desc">
                Cleaned datasets are saved under <b>data/processed/products</b>,
                <b>data/processed/sales</b>, and <b>data/processed/reviews</b>.
                This Streamlit dashboard now reads from these PySpark-generated Parquet outputs.
            </div>
        </div>

        <div class="pipeline-card">
            <div class="pipeline-step">4. SQL KPI Layer</div>
            <div class="pipeline-desc">
                SQL scripts define relational tables, KPI queries, and data quality checks for revenue,
                product performance, sentiment distribution, monthly trends, and validation checks.
            </div>
        </div>

        <div class="pipeline-card">
            <div class="pipeline-step">5. Databricks-Ready Workflow</div>
            <div class="pipeline-desc">
                The <b>databricks/</b> folder includes Bronze, Silver, and Gold workflow files that show how
                this local pipeline can scale into Databricks using PySpark, Spark SQL, and Delta-style tables.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Processed Dataset Preview</div>', unsafe_allow_html=True)

    preview_tab1, preview_tab2, preview_tab3 = st.tabs(
        ["Products", "Sales", "Reviews"]
    )

    with preview_tab1:
        st.dataframe(products_df.head(20), use_container_width=True)

    with preview_tab2:
        st.dataframe(sales_df.head(20), use_container_width=True)

    with preview_tab3:
        st.dataframe(reviews_df.head(20), use_container_width=True)

    st.markdown('<div class="section-title">Data Quality Snapshot</div>', unsafe_allow_html=True)

    dq_rows = []

    dq_rows.append(
        {
            "check_name": "Products row count",
            "value": len(products_df),
            "status": "Pass" if len(products_df) > 0 else "Fail",
        }
    )

    dq_rows.append(
        {
            "check_name": "Sales row count",
            "value": len(sales_df),
            "status": "Pass" if len(sales_df) > 0 else "Fail",
        }
    )

    dq_rows.append(
        {
            "check_name": "Reviews row count",
            "value": len(reviews_df),
            "status": "Pass" if len(reviews_df) > 0 else "Fail",
        }
    )

    dq_rows.append(
        {
            "check_name": "Missing sales dates",
            "value": int(sales_df["sale_date"].isna().sum()) if "sale_date" in sales_df.columns else "N/A",
            "status": "Pass"
            if "sale_date" in sales_df.columns and sales_df["sale_date"].isna().sum() == 0
            else "Review",
        }
    )

    dq_rows.append(
        {
            "check_name": "Invalid or missing revenue rows",
            "value": int((sales_df["total_sales"].isna() | (sales_df["total_sales"] <= 0)).sum())
            if "total_sales" in sales_df.columns
            else "N/A",
            "status": "Pass"
            if "total_sales" in sales_df.columns
            and (sales_df["total_sales"].isna() | (sales_df["total_sales"] <= 0)).sum() == 0
            else "Review",
        }
    )

    dq_rows.append(
        {
            "check_name": "Invalid or missing ratings",
            "value": int((reviews_df["rating"].isna() | (reviews_df["rating"] < 1) | (reviews_df["rating"] > 5)).sum())
            if "rating" in reviews_df.columns
            else "N/A",
            "status": "Pass"
            if "rating" in reviews_df.columns
            and (reviews_df["rating"].isna() | (reviews_df["rating"] < 1) | (reviews_df["rating"] > 5)).sum() == 0
            else "Review",
        }
    )

    dq_df = pd.DataFrame(dq_rows)
    st.dataframe(dq_df, use_container_width=True)


# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        Built by Heeya Amin · Nike-inspired data engineering and analytics project for portfolio and educational use · Not affiliated with Nike, Inc.
    </div>
    """,
    unsafe_allow_html=True,
)