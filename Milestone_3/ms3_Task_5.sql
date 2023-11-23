-- Changing removed column into boolean values
UPDATE dim_products
SET removed = CASE
    WHEN removed = 'Still_avaliable' THEN TRUE
    WHEN removed = 'Removed' THEN FALSE
    ELSE NULL -- Handle other cases if needed
END;

-- Renaming removed to still_available
ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;

-- Change data types
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT,
ALTER COLUMN EAN TYPE VARCHAR(20), -- 20 chars covers longest EAN string with extra space
ALTER COLUMN product_code TYPE VARCHAR(12), -- 12 chars covers longest product_code string
ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
ALTER COLUMN uuid TYPE UUID USING uuid:UUID,
ALTER COLUMN still_available TYPE BOOL,
ALTER COLUMN weight_class TYPE VARCHAR(15); -- Covers longest weight class string with extra room