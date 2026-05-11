# NikePulse: Product Intelligence & Demand Analytics Dashboard

NikePulse is a Nike-inspired end-to-end data analytics project that combines data engineering, exploratory analytics, customer sentiment analysis, machine learning, and dashboard development.

I built this project to explore how a product-driven sportswear company could use data to understand product performance, regional demand, customer satisfaction, sales channels, and future demand patterns.

This project is independent and created for educational and portfolio purposes. It is not affiliated with Nike, Inc.

---

## Project Article

I wrote a full Medium article explaining the idea, data flow, dashboard, modeling approach, and learnings behind this project:

**Read the article here:**  
https://medium.com/@heeyaamin1/building-nikepulse-a-nike-inspired-product-intelligence-and-demand-analytics-dashboard-69cb59d883ba

---

## What This Project Does

NikePulse helps answer questions like:

- Which product categories generate the most revenue?
- Which regions and states show the strongest demand?
- Which sales methods perform best across markets?
- What do customer reviews reveal about product satisfaction?
- Can machine learning help predict product unit sales?
- How can raw datasets be converted into an interactive dashboard?

---

## Dashboard Pages

The Streamlit dashboard includes five main sections:

1. **Executive Overview**  
   High-level KPIs including revenue, units sold, average price, ratings, top region, top product category, and monthly sales trends.

2. **Sales Performance**  
   Product-level and retailer-level analysis, including revenue by product, units sold, price vs demand, and retailer performance.

3. **Regional Insights**  
   Region and state-level demand analysis, including revenue by region, top states, and sales method performance.

4. **Customer Sentiment**  
   NLP-based review sentiment analysis using VADER, including positive/negative review rates, rating distribution, and sample reviews.

5. **Demand Prediction**  
   Machine learning model results for predicting units sold using sales, pricing, channel, product, region, and seasonal features.

---

## Tech Stack

- Python
- pandas
- NumPy
- scikit-learn
- matplotlib
- Plotly
- Streamlit
- VADER Sentiment Analysis
- joblib
- Git/GitHub

---

## Project Workflow

```text
Raw Kaggle Datasets
        ↓
Data Loading
        ↓
Data Cleaning & Standardization
        ↓
Processed Datasets
        ↓
EDA + Sales Visualizations
        ↓
Sentiment Analysis + Demand Prediction
        ↓
Interactive Streamlit Dashboard

Datasets

This project uses publicly available Kaggle datasets related to:

Nike product catalog data
Nike sales transaction data
Nike shoe review data

Raw datasets are not included in this repository. Place them inside:

data/raw/

Expected file names:

nike_products.csv
nike_sales.csv
nike_shoe_reviews.csv
How to Run Locally
1. Clone the repository
git clone https://github.com/HeeyaAmin/nikepulse-product-intelligence.git
cd nikepulse-product-intelligence
2. Create and activate environment
conda create -n nikepulse python=3.11 -y
conda activate nikepulse
3. Install dependencies
pip install -r requirements.txt
4. Add raw datasets

Place the Kaggle CSV files inside:

data/raw/
5. Run the pipeline
python src/ingestion/load_data.py
python src/cleaning/clean_data.py
python src/features/eda_summary.py
python src/features/generate_charts.py
python src/models/sentiment_analysis.py
python src/features/generate_sentiment_charts.py
python src/models/demand_prediction.py
6. Launch dashboard
streamlit run dashboard/app.py
Machine Learning

The demand prediction model predicts units_sold using:

Product category
Region
Retailer
Sales method
State
Price per unit
Year
Month
Quarter

Models compared:

Linear Regression
Random Forest Regressor

Evaluation metrics:

MAE
RMSE
R² Score
What I Learned

This project helped me practice building a complete data project from raw data to final dashboard. It strengthened my understanding of data cleaning, feature engineering, customer sentiment analysis, machine learning evaluation, and business-focused dashboard storytelling.

Future Improvements
Add PostgreSQL integration
Build a formal star schema
Add SQL analysis queries
Add Airflow or Prefect orchestration
Deploy the Streamlit dashboard
Add SHAP model explainability
Add competitor analysis
Add sneaker resale or hype-score analysis
Author

Heeya Amin
MS Data Science, Indiana University Bloomington

Portfolio: https://heeya-portfolio.vercel.app

GitHub: https://github.com/HeeyaAmin

LinkedIn: https://www.linkedin.com/in/heeya-amin/