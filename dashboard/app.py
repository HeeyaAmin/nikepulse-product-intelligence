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
    /* Main app background */
    .stApp {
        background-color: #f7f7f7;
        color: #111111;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111111;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Sidebar widgets */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #1f1f1f;
        border-color: #444444;
    }

    /* Hero card */
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

    /* Section headers */
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

    /* Metric cards */
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

    /* Plot containers */
    div[data-testid="stPlotlyChart"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
    }

    /* Image cards */
    div[data-testid="stImage"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }

    /* Horizontal rule */
    hr {
        border: none;
        border-top: 1px solid #dddddd;
        margin: 1.5rem 0;
    }

    /* Small info cards */
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

    sales_path = project_root / "data" / "processed" / "clean_sales.csv"
    reviews_path = project_root / "data" / "processed" / "reviews_with_sentiment.csv"
    products_path = project_root / "data" / "processed" / "clean_products.csv"

    missing_files = []

    if not sales_path.exists():
        missing_files.append(str(sales_path))

    if not reviews_path.exists():
        missing_files.append(str(reviews_path))

    if not products_path.exists():
        missing_files.append(str(products_path))

    if missing_files:
        st.error("Some required files are missing. Please generate them first.")
        st.write(missing_files)
        st.stop()

    sales_df = pd.read_csv(sales_path)
    reviews_df = pd.read_csv(reviews_path)
    products_df = pd.read_csv(products_path)

    return sales_df, reviews_df, products_df, project_root


sales_df, reviews_df, products_df, project_root = load_data()


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
    return f"${value:,.0f}"


# ============================================================
# Hero Section
# ============================================================
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-tag">Nike-inspired data intelligence platform</div>
        <div class="hero-title">NikePulse</div>
        <div class="hero-subtitle">
            A product, sales, consumer sentiment, and demand analytics platform built to explore how data can support
            sport-inspired product decisions, regional strategy, pricing insights, and customer experience.
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
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Control Room")

selected_region = st.sidebar.multiselect(
    "Region",
    options=sorted(sales_df["region"].dropna().unique()),
    default=sorted(sales_df["region"].dropna().unique()),
)

selected_product = st.sidebar.multiselect(
    "Product",
    options=sorted(sales_df["product"].dropna().unique()),
    default=sorted(sales_df["product"].dropna().unique()),
)

selected_sales_method = st.sidebar.multiselect(
    "Sales Method",
    options=sorted(sales_df["sales_method"].dropna().unique()),
    default=sorted(sales_df["sales_method"].dropna().unique()),
)

filtered_sales = sales_df[
    (sales_df["region"].isin(selected_region))
    & (sales_df["product"].isin(selected_product))
    & (sales_df["sales_method"].isin(selected_sales_method))
].copy()

if filtered_sales.empty:
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
    avg_rating = reviews_df["rating"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", format_currency(total_revenue))
    col2.metric("Units Sold", f"{total_units:,.0f}")
    col3.metric("Avg. Price / Unit", f"${avg_price:,.2f}")
    col4.metric("Avg. Review Rating", f"{avg_rating:.2f}/5")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        monthly_sales = (
            filtered_sales.groupby(["year", "month"])["total_sales"]
            .sum()
            .reset_index()
        )

        monthly_sales["year_month"] = (
            monthly_sales["year"].astype(str)
            + "-"
            + monthly_sales["month"].astype(str).str.zfill(2)
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

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">Top Region</div>
                <div class="insight-value">{top_region.index[0]}</div>
            </div>
            <div class="insight-card">
                <div class="insight-title">Top Product Category</div>
                <div class="insight-value">{top_product.index[0]}</div>
            </div>
            <div class="insight-card">
                <div class="insight-title">Top Sales Method</div>
                <div class="insight-value">{top_method.index[0]}</div>
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

        - Product category  
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
# Footer
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        Built by Heeya Amin · Nike-inspired analytics project for portfolio and educational use · Not affiliated with Nike, Inc.
    </div>
    """,
    unsafe_allow_html=True,
)