-- olist_full_reset_load.sql

DROP SCHEMA IF EXISTS olist CASCADE;
CREATE SCHEMA olist;
SET search_path TO olist, public;
SET client_encoding TO 'UTF8';

-- 1) GEOLOCATION (prefix có thể trùng)
CREATE TABLE olist.olist_geolocation (
  geolocation_id BIGSERIAL PRIMARY KEY,
  geolocation_zip_code_prefix VARCHAR(10) NOT NULL,
  geolocation_lat DOUBLE PRECISION,
  geolocation_lng DOUBLE PRECISION,
  geolocation_city VARCHAR(100),
  geolocation_state VARCHAR(2)
);

-- 2) ZIP PREFIX (đích FK)
CREATE TABLE olist.olist_zip_prefix (
  zip_code_prefix VARCHAR(10) PRIMARY KEY,
  city  VARCHAR(100),
  state VARCHAR(2)
);

-- 3) CUSTOMERS (FK deferred để load an toàn)
CREATE TABLE olist.olist_customers (
  customer_id VARCHAR(50) PRIMARY KEY,
  customer_unique_id VARCHAR(50) NOT NULL,
  customer_zip_code_prefix VARCHAR(10) NOT NULL
    REFERENCES olist.olist_zip_prefix(zip_code_prefix) DEFERRABLE INITIALLY DEFERRED,
  customer_city  VARCHAR(100),
  customer_state VARCHAR(2)
);

-- 4) SELLERS (FK deferred)
CREATE TABLE olist.olist_sellers (
  seller_id VARCHAR(50) PRIMARY KEY,
  seller_zip_code_prefix VARCHAR(10) NOT NULL
    REFERENCES olist.olist_zip_prefix(zip_code_prefix) DEFERRABLE INITIALLY DEFERRED,
  seller_city  VARCHAR(100),
  seller_state VARCHAR(2)
);

-- 5) PRODUCTS
CREATE TABLE olist.olist_products (
  product_id VARCHAR(50) PRIMARY KEY,
  product_category_name VARCHAR(100),
  product_name_length INTEGER,
  product_description_length INTEGER,
  product_photos_qty INTEGER,
  product_weight_g INTEGER,
  product_length_cm INTEGER,
  product_height_cm INTEGER,
  product_width_cm INTEGER
);

-- 6) ORDERS
CREATE TABLE olist.olist_orders (
  order_id VARCHAR(50) PRIMARY KEY,
  customer_id VARCHAR(50) NOT NULL REFERENCES olist.olist_customers(customer_id),
  order_status VARCHAR(20),
  order_purchase_timestamp TIMESTAMPTZ,
  order_approved_at TIMESTAMPTZ,
  order_delivered_carrier_date TIMESTAMPTZ,
  order_delivered_customer_date TIMESTAMPTZ,
  order_estimated_delivery_date TIMESTAMPTZ
);

-- 7) ORDER PAYMENTS
CREATE TABLE olist.olist_order_payments (
  order_id VARCHAR(50) NOT NULL REFERENCES olist.olist_orders(order_id) ON DELETE CASCADE,
  payment_sequential INTEGER NOT NULL,
  payment_type VARCHAR(20),
  payment_installments INTEGER,
  payment_value NUMERIC(10,2),
  PRIMARY KEY (order_id, payment_sequential)
);

-- 8) ORDER REVIEWS (review_id là duy nhất trong data)
CREATE TABLE olist.olist_order_reviews (
  review_id VARCHAR(50) PRIMARY KEY,
  order_id VARCHAR(50) NOT NULL REFERENCES olist.olist_orders(order_id) ON DELETE CASCADE,
  review_score INTEGER,
  review_comment_title VARCHAR(255),
  review_comment_message TEXT,
  review_creation_date TIMESTAMPTZ,
  review_answer_timestamp TIMESTAMPTZ
);

-- 9) ORDER ITEMS
CREATE TABLE olist.olist_order_items (
  order_id VARCHAR(50) NOT NULL REFERENCES olist.olist_orders(order_id) ON DELETE CASCADE,
  order_item_id INTEGER NOT NULL,
  product_id VARCHAR(50) NOT NULL REFERENCES olist.olist_products(product_id),
  seller_id VARCHAR(50) NOT NULL REFERENCES olist.olist_sellers(seller_id),
  shipping_limit_date TIMESTAMPTZ,
  price NUMERIC(10,2),
  freight_value NUMERIC(10,2),
  PRIMARY KEY (order_id, order_item_id)
);

-- 10) TRANSLATION
CREATE TABLE olist.olist_product_category_translation (
  product_category_name VARCHAR(100) PRIMARY KEY,
  product_category_name_english VARCHAR(100)
);

\echo ==== LOAD DATA (IN ONE TX) ====
BEGIN;
SET CONSTRAINTS ALL DEFERRED;

-- GEOLOCATION
\copy olist.olist_geolocation(geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state) FROM '/import/olist_geolocation_dataset.csv' CSV HEADER NULL ''

-- ZIP PREFIX từ GEOLOCATION (idempotent)
INSERT INTO olist.olist_zip_prefix (zip_code_prefix, city, state)
SELECT DISTINCT ON (geolocation_zip_code_prefix)
       geolocation_zip_code_prefix,
       NULLIF(geolocation_city, ''),
       NULLIF(geolocation_state, '')
FROM olist.olist_geolocation
WHERE geolocation_zip_code_prefix IS NOT NULL
ORDER BY geolocation_zip_code_prefix, geolocation_city NULLS LAST
ON CONFLICT (zip_code_prefix) DO UPDATE
SET city  = COALESCE(EXCLUDED.city,  olist.olist_zip_prefix.city),
    state = COALESCE(EXCLUDED.state, olist.olist_zip_prefix.state);

-- CUSTOMERS
\copy olist.olist_customers(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) FROM '/import/olist_customers_dataset.csv' CSV HEADER NULL ''

-- Bổ sung mọi prefix còn thiếu từ CUSTOMERS
INSERT INTO olist.olist_zip_prefix (zip_code_prefix, city, state)
SELECT DISTINCT c.customer_zip_code_prefix,
       NULLIF(c.customer_city, ''),
       NULLIF(c.customer_state, '')
FROM olist.olist_customers c
LEFT JOIN olist.olist_zip_prefix z ON z.zip_code_prefix = c.customer_zip_code_prefix
WHERE z.zip_code_prefix IS NULL;

-- SELLERS
\copy olist.olist_sellers(seller_id, seller_zip_code_prefix, seller_city, seller_state) FROM '/import/olist_sellers_dataset.csv' CSV HEADER NULL ''

-- Bổ sung mọi prefix còn thiếu từ SELLERS
INSERT INTO olist.olist_zip_prefix (zip_code_prefix, city, state)
SELECT DISTINCT s.seller_zip_code_prefix,
       NULLIF(s.seller_city, ''),
       NULLIF(s.seller_state, '')
FROM olist.olist_sellers s
LEFT JOIN olist.olist_zip_prefix z ON z.zip_code_prefix = s.seller_zip_code_prefix
WHERE z.zip_code_prefix IS NULL;

-- PRODUCTS
\copy olist.olist_products(product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm) FROM '/import/olist_products_dataset.csv' CSV HEADER NULL ''

-- ORDERS
\copy olist.olist_orders(order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date) FROM '/import/olist_orders_dataset.csv' CSV HEADER NULL ''

-- PAYMENTS
\copy olist.olist_order_payments(order_id, payment_sequential, payment_type, payment_installments, payment_value) FROM '/import/olist_order_payments_dataset.csv' CSV HEADER NULL ''

-- REVIEWS: nạp qua bảng tạm và dedupe theo review_id (giữ bản mới nhất)
CREATE TEMP TABLE stg_reviews(
  review_id VARCHAR(50),
  order_id VARCHAR(50),
  review_score INTEGER,
  review_comment_title VARCHAR(255),
  review_comment_message TEXT,
  review_creation_date TIMESTAMPTZ,
  review_answer_timestamp TIMESTAMPTZ
);
\copy stg_reviews(review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp) FROM '/import/olist_order_reviews_dataset.csv' CSV HEADER NULL ''

INSERT INTO olist.olist_order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp)
SELECT review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp
FROM (
  SELECT s.*,
         ROW_NUMBER() OVER (
           PARTITION BY review_id
           ORDER BY review_answer_timestamp DESC NULLS LAST, review_creation_date DESC NULLS LAST
         ) AS rn
  FROM stg_reviews s
) t
WHERE rn = 1
ON CONFLICT (review_id) DO NOTHING;

-- ORDER ITEMS
\copy olist.olist_order_items(order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value) FROM '/import/olist_order_items_dataset.csv' CSV HEADER NULL ''

-- TRANSLATION
-- (Dùng staging + upsert để an toàn)
CREATE TEMP TABLE stg_trans(
  product_category_name text,
  product_category_name_english text
);
\copy stg_trans(product_category_name, product_category_name_english) FROM '/import/olist_product_category_translation.csv' CSV HEADER NULL ''
INSERT INTO olist.olist_product_category_translation(product_category_name, product_category_name_english)
SELECT product_category_name, product_category_name_english
FROM stg_trans
ON CONFLICT (product_category_name) DO UPDATE
SET product_category_name_english = EXCLUDED.product_category_name_english;

COMMIT;

ANALYZE;

-- (Tuỳ chọn) Index gợi ý cho join và truy vấn phổ biến
-- CREATE INDEX IF NOT EXISTS idx_geo_zip           ON olist.olist_geolocation(geolocation_zip_code_prefix);
-- CREATE INDEX IF NOT EXISTS idx_customers_zip     ON olist.olist_customers(customer_zip_code_prefix);
-- CREATE INDEX IF NOT EXISTS idx_sellers_zip       ON olist.olist_sellers(seller_zip_code_prefix);
-- CREATE INDEX IF NOT EXISTS idx_orders_customer   ON olist.olist_orders(customer_id);
-- CREATE INDEX IF NOT EXISTS idx_orders_ts         ON olist.olist_orders(order_purchase_timestamp);
-- CREATE INDEX IF NOT EXISTS idx_items_order       ON olist.olist_order_items(order_id);
-- CREATE INDEX IF NOT EXISTS idx_items_product     ON olist.olist_order_items(product_id);
-- CREATE INDEX IF NOT EXISTS idx_items_seller      ON olist.olist_order_items(seller_id);
-- CREATE INDEX IF NOT EXISTS idx_reviews_score     ON olist.olist_order_reviews(review_score);
