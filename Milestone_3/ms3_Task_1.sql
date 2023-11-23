-- Change data type of date_uuid column
ALTER TABLE orders_table
ALTER COLUMN date_uuid SET DATA TYPE UUID USING date_uuid::UUID;

-- Change data type of user_uuid column
ALTER COLUMN user_uuid SET DATA TYPE UUID USING user_uuid::UUID;

-- Change data type of card_number column with VARCHAR(?) (replace ? with the maximum length)
ALTER COLUMN card_number SET DATA TYPE VARCHAR(20);

-- Change data type of store_code column with VARCHAR(?) (replace ? with the maximum length)
ALTER COLUMN store_code SET DATA TYPE VARCHAR(15);

-- Change data type of product_code column with VARCHAR(?) (replace ? with the maximum length)
ALTER COLUMN product_code SET DATA TYPE VARCHAR(12);

-- Change data type of product_quantity column
ALTER COLUMN product_quantity SET DATA TYPE SMALLINT;