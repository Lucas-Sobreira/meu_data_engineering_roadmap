SELECT SUM(od.unit_price * od.quantity * (1-od.discount)) AS total_revenue_1997
FROM order_details od
INNER JOIN orders o on o.order_id = od.order_id
WHERE EXTRACT(YEAR FROM o.order_date) = 1997;