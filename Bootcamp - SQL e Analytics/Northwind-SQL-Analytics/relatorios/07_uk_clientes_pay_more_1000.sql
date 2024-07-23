SELECT 
	c.contact_name, 
	SUM(od.unit_price * od.quantity * (1.0 - od.discount) * 100) / 100 AS payments
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.customer_id
INNER JOIN order_details AS od ON od.order_id = o.order_id
WHERE LOWER(c.country) = 'uk'
GROUP BY c.contact_name
HAVING SUM(od.unit_price * od.quantity * (1.0 - od.discount)) > 1000
ORDER BY payments DESC;