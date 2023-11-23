SELECT 
	ROUND((SUM(product_price * product_quantity))::numeric,2) as total_sales,
	store_type,
	country_code
FROM
	orders_table o
JOIN
	dim_store_details st ON o.store_code = st.store_code
JOIN
	dim_products prod ON o.product_code = prod.product_code
WHERE
	country_code LIKE 'DE'
GROUP BY 
	store_type, country_code
ORDER BY
	total_sales ASC