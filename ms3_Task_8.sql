-- Add primary key to dim_users table using user_uuid as primary key
ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);

-- Add primary key to dim_card_details table using card_number as primary key
ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);

-- Add primary key to dim_store_details table using store_code as primary key
ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);

-- Add primary key to dim_products table using product_code as primary key
ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);

-- Add primary key to dim_date_times table using date_uuid as primary key
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);