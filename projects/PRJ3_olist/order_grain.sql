WITH item_summary AS (
 SELECT order_id,COUNT(*) AS item_count,COUNT(DISTINCT seller_id) AS sellers,
 SUM(price) AS item_value,SUM(freight_value) AS freight_value FROM items GROUP BY order_id
), payment_summary AS (
 SELECT order_id,COUNT(*) AS payment_rows,SUM(payment_value) AS paid FROM payments GROUP BY order_id
), review_summary AS (
 SELECT order_id,COUNT(*) AS review_rows,AVG(review_score) AS mean_review_score FROM reviews GROUP BY order_id
)
SELECT o.*, c.customer_state,i.item_count,i.sellers,i.item_value,i.freight_value,p.payment_rows,p.paid,r.review_rows,r.mean_review_score
FROM orders o LEFT JOIN customers c USING(customer_id)
LEFT JOIN item_summary i USING(order_id) LEFT JOIN payment_summary p USING(order_id)
LEFT JOIN review_summary r USING(order_id)