WITH total_per_client_group AS (
SELECT 
	c.customer_id,
	company_name, 
	SUM(od.unit_price * od.quantity * (1-od.discount)) AS total, 
	NTILE(5) OVER (ORDER BY SUM(od.unit_price * od.quantity * (1-od.discount)) DESC) AS n_grupo
FROM customers AS c 
INNER JOIN orders AS o ON o.customer_id = c.customer_id
INNER JOIN order_details AS od ON od.order_id = o.order_id
GROUP BY c.customer_id
ORDER BY total DESC
	)

SELECT * 
FROM total_per_client_group
WHERE n_grupo >= 3;