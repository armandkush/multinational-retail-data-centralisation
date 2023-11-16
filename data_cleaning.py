import pandas as pd
import phonenumbers
import numpy as np
import re

class DataCleaning:
    def __init__(self):
        pass
    
    def format_phone_number(self, number, region):
        try:
            phone_number = phonenumbers.parse(number, region)
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            return None 
    

    def clean_user_data(self, user_data_df):
        try:
            # Drop rows with missing values
            user_data_df.dropna(inplace=True)

            #Cleaning rows with erroneous data (invalid data)
            pattern1 = r'^[0-9]*[A-Z0-9]+[A-Z0-9]*$'
            mask1 = user_data_df['first_name'].str.match(pattern1)
            user_data_df = user_data_df[~mask1]

            # Clean date of birth column
            user_data_df['date_of_birth'] = pd.to_datetime(user_data_df['date_of_birth'], errors='coerce')
            user_data_df = user_data_df.dropna(subset=['date_of_birth'])
            
            # Clean join date column
            user_data_df['join_date'] = pd.to_datetime(user_data_df['join_date'], errors='coerce')
            user_data_df = user_data_df.dropna(subset=['join_date'])

            #Cleaning phone numbers column
            user_data_df['phone_number'] = user_data_df.apply(lambda row: self.format_phone_number(row['phone_number'], row['country_code']), axis=1)

            # Resetting index
            user_data_df.reset_index(drop=True, inplace=True)

            # Return the cleaned DataFrame
            return user_data_df
        
        except Exception as e:
            print(f"Error cleaning user data: {str(e)}")
            return None
        

    def clean_card_data(self, input_df):
        try:
            # Drop extra columns from concat
            input_df = input_df.drop(['card_number expiry_date', 'Unnamed: 0'], axis=1)

            # Drop rows with missing values
            input_df.dropna(inplace=True)

            # Clean date_payment_confirmed column
            input_df['date_payment_confirmed'] = pd.to_datetime(input_df['date_payment_confirmed'], errors='coerce')
            input_df = input_df.dropna(subset=['date_payment_confirmed'])

            #Cleaning rows with erroneous data (invalid data)
            input_df['card_number'] = input_df['card_number'].astype(str)

            # Keep only rows where the cardnumber has purely numeric data
            input_df = input_df[input_df['card_number'].str.isnumeric()]

            # Convert the cardnumber back to int64
            input_df['card_number'] = input_df['card_number'].astype('int64')

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df
            
        
        except Exception as f:
            print(f"Error cleaning card data: {str(f)}")
            return None
        
    def clean_store_data(self, input_df):
        try:
            # Drop lat column 
            input_df = input_df.drop(['lat'], axis=1)

            # Drop rows with missing values
            input_df.dropna(inplace=True)

            #Cleaning rows with erroneous data (invalid data) using staff numbers as datum
            input_df['staff_numbers'] = input_df['staff_numbers'].astype(str)

            # Keep only rows where the cardnumber has purely numeric data
            input_df = input_df[input_df['staff_numbers'].str.isnumeric()]

            # Convert the cardnumber back to int64
            input_df['staff_numbers'] = input_df['staff_numbers'].astype('int64')

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df
        

        except Exception as f:
            print(f"Error cleaning card data: {str(f)}")
            return None
        
    
    def convert_product_weights(self, input_df):
        try:

            def convert_to_kg(weight):
                # Convert data to string for regex
                weight_str = str(weight)

                if weight_str == 'nan' or weight_str == 'None':
                    return None


            # Using regular expression to extract the number and the unit
                match = re.match(r"(\d+\.?\d*)\s*(\w+)", weight_str)
                if match:
                    value, unit = match.groups()
                    value = float(value)
                    
                
                    # Defining conversion factors
                    if unit in ['g', 'ml']:  # Assuming 1g = 1ml
                        return round((value / 1000), 3)  # Convert g and ml to kg
                    elif unit == 'kg':
                        return round(value,3)
                    
                    else:
                        # If unit is unrecognized
                        return None
                
                else:
                    try:
                        return round(float(weight_str),3)
                    except ValueError:
                        return None

            input_df['weight'] = input_df['weight'].apply(convert_to_kg)
            return input_df

        except Exception as g:
            print(f"Error converting product weight data: {str(g)}")
            return None


    def clean_product_data(self, input_df):
        try:
            # Drop Unnamed:0 column 
            input_df = input_df.drop(['Unnamed: 0'], axis=1)

            # Drop rows with missing values
            input_df.dropna(inplace=True)

            #Cleaning rows with erroneous data (invalid data) using EAN as datum
            input_df['EAN'] = input_df['EAN'].astype(str)

            # Keep only rows where the EAN has purely numeric data
            input_df = input_df[input_df['EAN'].str.isnumeric()]

            # Convert the EAN back to str
            input_df['EAN'] = input_df['EAN'].astype('str')

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df
        
        except Exception as h:
            print(f"Error cleaning product data: {str(h)}")

    def clean_orders_data(self, input_df):
        try:
            # Drop level_0, first_name, last_name, 1 column 
            input_df = input_df.drop(['level_0','first_name','last_name','1'], axis=1)

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df

        except Exception as i:
            print(f"Error cleaning order data table: {str(i)}") 

    def clean_date_time_data(self, input_df):
        try:

            # Replace NULL with na
            input_df.replace('NULL', np.nan, inplace= True)

            # Drop rows with missing values
            input_df.dropna(inplace=True)

            #Cleaning rows with erroneous data (invalid data) using time_period as datum
            input_df['time_period'] = input_df['time_period'].astype(str)

            # Keep only rows where the EAN has purely numeric data
            input_df = input_df[input_df['time_period'].str.isalpha()]

            # Convert the EAN back to str
            input_df['time_period'] = input_df['time_period'].astype(str)

            # Rename timestamp to time
            input_df.rename(columns = {'timestamp':'time'}, inplace=True) 

            # Combine timestamps into one column called complete_timestamp
            input_df['timestamp'] = pd.to_datetime(input_df[['year', 'month','day']].assign(hour = input_df['time'].str.split(':').str[0].astype('int64'), minute = input_df['time'].str.split(':').str[1].astype('int64'), second = input_df['time'].str.split(':').str[2].astype('int64')))

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df

        except Exception as j:
            print(f"Error cleaning date time data: {str(j)}")
