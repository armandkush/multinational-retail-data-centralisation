select 
	COUNT(*) as number_of_sales,
	SUM(product_quantity) AS product_quantity_count,
	CASE 
		WHEN locality = 'N/A' THEN 'Web'
		ELSE 'Offline'
	END AS location
FROM
	orders_table o
JOIN
	dim_store_details st ON o.store_code = st.store_code
JOIN
	dim_products prod ON o.product_code = prod.product_code
GROUP BY 
	CASE 
		WHEN locality = 'N/A' THEN 'Web'
		ELSE 'Offline'
	END
ORDER BY 
	number_of_sales ASC