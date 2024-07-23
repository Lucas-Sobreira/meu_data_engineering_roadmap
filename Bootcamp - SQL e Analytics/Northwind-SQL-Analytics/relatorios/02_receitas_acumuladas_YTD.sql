WITH receita_mensal_ano AS (
SELECT 
	EXTRACT(YEAR FROM o.order_date) AS ano, 
	EXTRACT(MONTH FROM o.order_date) AS mes,
	SUM(od.unit_price * od.quantity * (1-od.discount)) AS receita_mensal
FROM order_details od
INNER JOIN orders o on o.order_id = od.order_id
GROUP BY 
	EXTRACT(YEAR FROM o.order_date),
	EXTRACT(MONTH FROM o.order_date)
ORDER BY 
	EXTRACT(YEAR FROM o.order_date),
	EXTRACT(MONTH FROM o.order_date)
)

SELECT 
	ano,
	mes, 
	receita_mensal, 
	(receita_mensal - LAG(receita_mensal) OVER (PARTITION BY ano ORDER BY mes)) as diferenca_mes,
	SUM(receita_mensal) OVER (PARTITION BY ano ORDER BY mes) as receita_ytd,
	((receita_mensal - LAG(receita_mensal) OVER (PARTITION BY ano ORDER BY mes)) / LAG(receita_mensal) OVER (PARTITION BY ano ORDER BY mes)) * 100 as percent_dif_mes
FROM receita_mensal_ano
ORDER BY 
	ano, 
	mes;