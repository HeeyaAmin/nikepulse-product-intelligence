# NikePulse: Product Intelligence & Data Engineering Dashboard

NikePulse is a Nike-inspired end-to-end **data engineering, analytics, machine learning, and dashboarding project**.

I built this project to explore how a product-driven sportswear company could use data pipelines, SQL-based KPI logic, customer sentiment analysis, machine learning, and interactive dashboards to understand product performance, regional demand, sales channels, customer satisfaction, and future demand patterns.

This project is independent and created for educational and portfolio purposes. It is not affiliated with Nike, Inc.

## Live Demo
https://nikepulse.streamlit.app/

---

## Project Article

I wrote a full Medium article explaining the idea, data flow, dashboard, modeling approach, and learnings behind this project:

**Read the article here:**  
https://medium.com/@heeyaamin1/building-nikepulse-a-nike-inspired-product-intelligence-and-demand-analytics-dashboard-69cb59d883ba

---

## Project Purpose

The goal of NikePulse is to simulate a real-world product intelligence platform where raw product, sales, and customer review datasets are transformed into clean, analytics-ready datasets that support business KPIs, machine learning, and dashboard reporting.

This project is now structured more as a **data engineering project** with analytics and ML outputs.

It demonstrates:

- PySpark-based ETL processing
- SQL-based KPI analysis
- Databricks-style Bronze, Silver, and Gold architecture
- Data quality checks
- Parquet-based processed data storage
- Customer sentiment analysis
- Demand prediction modeling
- Streamlit dashboard development

---

## What This Project Does

NikePulse helps answer questions like:

- Which product categories generate the most revenue?
- Which regions and states show the strongest demand?
- Which sales methods perform best across markets?
- What do customer reviews reveal about product satisfaction?
- Which products receive the strongest positive or negative feedback?
- Can machine learning help predict product unit sales?
- How can raw retail datasets be converted into analytics-ready tables?
- How can PySpark, SQL, and Databricks-style workflows support product analytics?

---

## Dashboard Pages

The Streamlit dashboard includes six main sections:

1. **Executive Overview**  
   High-level KPIs including revenue, units sold, average price, average rating, top region, top product category, top sales method, and monthly sales trends.

2. **Sales Performance**  
   Product-level and retailer-level analysis, including revenue by product, units sold by product, price vs demand behavior, and retailer performance.

3. **Regional Insights**  
   Region and state-level demand analysis, including revenue by region, top states, units sold by state, and sales method performance by region.

4. **Customer Sentiment**  
   Review sentiment analysis using rating-based sentiment groups, including positive/negative review rates, rating distribution, average rating by sentiment, and sample customer reviews.

5. **Demand Prediction**  
   Machine learning model results for predicting units sold using product, region, retailer, sales method, state, price, and seasonal features.

6. **Data Engineering Pipeline**  
   Pipeline overview showing PySpark ETL processing, processed Parquet outputs, SQL KPI logic, Databricks-ready workflow design, and data quality checks.

---

## Tech Stack

### Programming & Analytics

- Python
- pandas
- NumPy
- scikit-learn
- joblib

### Data Engineering

- PySpark
- SQL
- PostgreSQL-ready schema design
- Parquet
- Databricks-ready workflow
- Delta Lake-style Bronze, Silver, and Gold architecture

### Visualization & Dashboarding

- Streamlit
- Plotly
- matplotlib

### NLP & Machine Learning

- VADER Sentiment Analysis
- Rating-based sentiment grouping
- Linear Regression
- Random Forest Regressor

### Development Tools

- Git
- GitHub
- Conda
- VS Code

---

## Project Architecture

```text
Raw Kaggle Datasets
        ↓
PySpark ETL Pipeline
        ↓
Cleaned Parquet Datasets
        ↓
SQL KPI + Data Quality Layer
        ↓
Machine Learning + Sentiment Analysis
        ↓
Interactive Streamlit Dashboard
        ↓
Databricks-Ready Bronze/Silver/Gold Workflow

Author

Heeya Amin
MS Data Science, Indiana University Bloomington

Portfolio: https://heeya-portfolio.vercel.app

GitHub: https://github.com/HeeyaAmin

LinkedIn: https://www.linkedin.com/in/heeya-amin/
