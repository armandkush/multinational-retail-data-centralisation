SELECT
    ROUND((SUM(product_price * product_quantity))::numeric,2) as total_sales, 
	year,
    month
FROM
    orders_table o
JOIN
    dim_date_times d ON o.date_uuid = d.date_uuid
JOIN
    dim_products prod ON o.product_code = prod.product_code
GROUP BY
    d.month, d.year
ORDER BY
    total_sales DESC
LIMIT 10