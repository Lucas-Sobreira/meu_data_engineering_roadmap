SELECT 
	p.product_name, 
	SUM(od.unit_price * od.quantity * (1.0 - od.discount)) AS sales
FROM products AS p
INNER JOIN order_details AS od ON od.product_id = p.product_id
GROUP BY p.product_name
ORDER BY sales DESC
LIMIT 10;