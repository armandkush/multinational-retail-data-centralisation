-- Merging both latitude columns
UPDATE dim_store_details
SET latitude = COALESCE(latitude, lat);

-- Drop lat column
ALTER TABLE dim_store_details
DROP COLUMN lat;

-- Set Latitude and longitude to NULL where 'N/A' and country code to 'N/A' where it is NULL
UPDATE dim_store_details
SET latitude = NULL, longitude = NULL, country_code = 'N/A'
WHERE latitude = 'N/A';

-- Change data type for dim_store_details
    ALTER TABLE store_details_table
        ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT,
        ALTER COLUMN locality TYPE VARCHAR(255),
        ALTER COLUMN store_code TYPE VARCHAR(15), 
        ALTER COLUMN staff_numbers TYPE SMALLINT,
        ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
        ALTER COLUMN store_type TYPE VARCHAR(255) USING NULLIF(store_type,'')::VARCHAR(255),
        ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT,
        ALTER COLUMN country_code TYPE VARCHAR(3), 
        ALTER COLUMN continent TYPE VARCHAR(255);   