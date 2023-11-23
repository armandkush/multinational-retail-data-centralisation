ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(20), -- 20 characters covers longest card number format with extra space
    ALTER COLUMN expiry_date TYPE VARCHAR(5), --5 characters covers fixed format of card expiry date
    ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;