DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    product_subtitle TEXT,
    brand TEXT,
    model TEXT,
    color TEXT,
    price NUMERIC,
    currency TEXT,
    availability TEXT,
    avg_rating NUMERIC,
    review_count INTEGER,
    available_sizes TEXT
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE,
    product_name TEXT,
    region TEXT,
    retailer TEXT,
    sales_method TEXT,
    state TEXT,
    price_per_unit NUMERIC,
    revenue NUMERIC,
    quantity INTEGER
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id TEXT,
    product_name TEXT,
    rating NUMERIC,
    review_date DATE,
    username TEXT,
    location TEXT,
    review_text TEXT,
    fit_feedback TEXT,
    comfort_feedback TEXT,
    recommend_feedback TEXT,
    rating_group TEXT
);