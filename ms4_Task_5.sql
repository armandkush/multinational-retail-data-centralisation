SELECT 
	st.store_type,
	ROUND((SUM(prod.product_price * o.product_quantity))::numeric,2) as total_sales,
	ROUND(((SUM(prod.product_price * o.product_quantity))::numeric/total.total_sales::numeric) * 100,2) AS percentage_total
FROM
    orders_table o
JOIN
    dim_products prod ON o.product_code = prod.product_code
JOIN 
    dim_store_details st ON o.store_code = st.store_code
CROSS JOIN (
	SELECT SUM(product_price * product_quantity) AS total_sales 
	FROM orders_table o_cross
	JOIN dim_products prod_cross ON o_cross.product_code = prod_cross.product_code
) AS total
GROUP BY
    total.total_sales, st.store_type
ORDER BY
    total_sales DESC