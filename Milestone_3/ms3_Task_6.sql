-- Update the data types for columns in dim_date_times
ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(2);
    ALTER COLUMN year TYPE VARCHAR(4);
    ALTER COLUMN day TYPE VARCHAR(2);
    ALTER COLUMN time_period TYPE VARCHAR(12); --12 characters cover longest time period string
    ALTER COLUMN date_uuid TYPE UUID;