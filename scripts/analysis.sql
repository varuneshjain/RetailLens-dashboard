USE retailens;

-- Top 5 Categories by Revenue
SELECT category, 
       ROUND(SUM(amount), 2) AS total_revenue,
       COUNT(*) AS total_orders
FROM amazon_sales
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 5;

-- Cancellation Rate by State
SELECT ship_state,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate
FROM amazon_sales
GROUP BY ship_state
ORDER BY cancellation_rate DESC
LIMIT 10;

--  Monthly Revenue Trend
SELECT month,
       month_num,
       ROUND(SUM(amount), 2) AS total_revenue,
       COUNT(*) AS total_orders,
       ROUND(AVG(amount), 2) AS avg_order_value
FROM amazon_sales
GROUP BY month, month_num
ORDER BY month_num;

-- Top 10 Cities by Orders
SELECT ship_city,
       COUNT(*) AS total_orders,
       ROUND(SUM(amount), 2) AS total_revenue
FROM amazon_sales
GROUP BY ship_city
ORDER BY total_orders DESC
LIMIT 10;

-- B2B vs B2C Revenue
SELECT b2b,
       COUNT(*) AS total_orders,
       ROUND(SUM(amount), 2) AS total_revenue,
       ROUND(AVG(amount), 2) AS avg_order_value
FROM amazon_sales
GROUP BY b2b;

-- Courier Status Analysis
SELECT courier_status,
       COUNT(*) AS total_orders,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM amazon_sales), 2) AS percentage
FROM amazon_sales
GROUP BY courier_status
ORDER BY total_orders DESC;