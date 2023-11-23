-- Removing £ sign from price column
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

-- Add weight_class column
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(15); -- 15 covers all characters of longest weight class with room to spare.

-- Update weight_class based on weight range
UPDATE dim_products
SET weight_class =
  CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck Required'
    ELSE NULL 

