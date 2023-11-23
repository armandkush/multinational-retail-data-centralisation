SELECT 
    CASE 
        WHEN country_code = 'N/A' THEN 'GB' 
        ELSE country_code 
    END AS country_code,
    SUM(staff_numbers) AS total_staff_numbers
FROM 
    dim_store_details
GROUP BY
    CASE 
        WHEN country_code = 'N/A' THEN 'GB' 
        ELSE country_code 
    END
ORDER BY
    total_staff_numbers DESC;