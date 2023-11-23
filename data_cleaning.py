import pandas as pd
import phonenumbers
import numpy as np
import re
from dateutil.parser import parse


class DataCleaning:
    '''

        This class is used to store methods for cleaning data for this project.
        
    '''
    def __init__(self):
        pass
    
    def format_phone_number(self, number, region):
        '''
       
        This function is used to format a specified number string according to it's region

        Returns:
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL) = Correctly formatted phone number.
            Exception = returns error code if the function fails.
        
        '''

        try:
            # Using phonenumbers library to format phone numbers correctly based on country code
            phone_number = phonenumbers.parse(number, region)
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            return None 
    
    def clean_user_data(self, input_df):
        '''
        
        This function is used clean user data for the user data table.
        Returns:
            return input_df = Cleaned data frame.
            Exception = returns error code if the function fails.
       
        '''
        try:
            # Drop rows with missing values
            input_df.dropna(inplace=True)

            #Cleaning rows with erroneous data (invalid data) using a regex pattern
            pattern1 = r'^[0-9]*[A-Z0-9]+[A-Z0-9]*$'
            mask1 = input_df['first_name'].str.match(pattern1)
            input_df = input_df[~mask1]

            # Clean date of birth column
            input_df['date_of_birth'] = input_df['date_of_birth'].apply(parse)
            input_df['date_of_birth'] = pd.to_datetime(input_df['date_of_birth'], infer_datetime_format=True, errors='coerce')
            input_df = input_df.dropna(subset=['date_of_birth'])
            
            # Clean join date column 
            input_df['join_date'] = input_df['join_date'].apply(parse)
            input_df['join_date'] = pd.to_datetime(input_df['join_date'], infer_datetime_format=True, errors='coerce')
            input_df = input_df.dropna(subset=['join_date'])

            #Cleaning phone numbers column
            input_df['phone_number'] = input_df['phone_number'].str.replace(r'[^0-9]', '')
            input_df['phone_number'] = input_df.apply(lambda row: self.format_phone_number(row['phone_number'], row['country_code']), axis=1)

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            # Return the cleaned DataFrame
            return input_df
        
        except Exception as error_details:
            print(f"Error cleaning user data: {str(error_details)}")
            return None
        
    def clean_card_data(self, input_df):
        '''
        
        This function is used clean card data for the card details table.
        Returns:
            return input_df = Cleaned data frame.
            Exception = returns error code if the function fails.
        
        '''
        try:

            # Replace 'NULL' with None for python compatibility
            input_df = input_df.replace('NULL', None)
            
            # Drop rows with missing values
            input_df.dropna(inplace=True)

            #Cleaning rows with erroneous data (invalid data) using expiry date
            input_df = input_df[input_df['expiry_date'].str.len() <= 6]

            #Cleaning card number to remove non numeric characters
            input_df['card_number'] = input_df['card_number'].astype(str)
            input_df['card_number'] = input_df['card_number'].str.replace('?','')
  
            # Clean date_payment_confirmed column
            # Change all YYYY-MM-DD to YYYY MM DD format
            input_df['date_payment_confirmed'] = input_df['date_payment_confirmed'].astype(str)
            input_df['date_payment_confirmed'] = input_df['date_payment_confirmed'].apply(parse)
            input_df['date_payment_confirmed'] = pd.to_datetime(input_df['date_payment_confirmed'], infer_datetime_format=True)

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)
            return input_df
            
        
        except Exception as error_details:
            print(f"Error cleaning card data: {str(error_details)}")
            return None

    def clean_store_data(self, input_df):
        '''
        
        This function is used clean store data for the store details table.
        Returns:
            return input_df = Cleaned data frame.
            Exception = returns error code if the function fails.
        
        '''
        try:
            # Defining error mapping for typos in continent column
            continent_mapping = {'eeEurope' : 'Europe', 'eeAmerica' : 'America'}

            # Cleaning erroneous data by removing country code rows longer than 4.
            input_df = input_df[input_df['country_code'].str.len() <= 4]

            # Fixing typos in continent column
            input_df['continent'] = input_df['continent'].map(continent_mapping).fillna(input_df['continent'])

            #Cleaning rows in staff_numbers
            input_df['staff_numbers'] = input_df['staff_numbers'].astype(str)
            
            # Remove non-numeric characters from staff_numbers column
            input_df['staff_numbers'] = input_df['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)

            # Keep only rows where the cardnumber has purely numeric data
            input_df = input_df[input_df['staff_numbers'].str.isnumeric()]

            # Convert the cardnumber back to int64
            input_df['staff_numbers'] = input_df['staff_numbers'].astype('int64')

            # Cleaning opening_dates
            input_df['opening_date'] = input_df['opening_date'].apply(parse)
            input_df['opening_date'] = pd.to_datetime(input_df['opening_date'], infer_datetime_format=True, errors='coerce')
            #input_df = input_df.dropna(subset=['opening_date'])
            
            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df
        

        except Exception as error_details:
            print(f"Error cleaning card data: {str(error_details)}")
            return None 

    def calculate_weight(self,value):
        '''
        
        This function is used to calculate weight for data with the format "A x B g"
        Returns:
            return str(value) = Calculated value in string format.
            Exception = returns error code if the function fails.
        
        '''
        try:
            # Using regex to find weight in "A x B g" format
            pattern_multi = r'(\d+) x (\d+)g'
            match = re.match(pattern_multi, value)
            if match:
                units = int(match.group(1))
                unit_weight = int(match.group(2))
                total_weight = units * unit_weight
                return str(f"{total_weight}g")
            else:
                return str(value)
            
        except Exception as error_details:
            print(f"Error calculating weight: {str(error_details)}")

    def convert_product_weights(self, input_df):
        '''

        This function is used to convert data of different units into kg. Returns None if unit is not recognized
        Returns:
            return input_df =  Data frame with corrected weight units.
            Exception = returns error code if the function fails.
        
        '''
        try:

            input_df['weight'] = input_df['weight'].apply(self.calculate_weight)
             
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
                    elif unit == 'oz':
                        return round((value*28.4)/1000, 3)
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

        except Exception as error_details:
            print(f"Error converting product weight data: {str(error_details)}")
            return None

    def clean_product_data(self, input_df):
        '''
        
        This function is used clean product data for the products table.
        Returns:
            return input_df = Cleaned data frame.
            Exception = returns error code if the function fails.
       
        '''
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
        
        except Exception as error_details:
            print(f"Error cleaning product data: {str(error_details)}")

    def clean_orders_data(self, input_df):
        '''
        
        This function is used clean orders data for the order details table.
        Returns:
            return input_df = Cleaned data frame.
            Exception = returns error code if the function fails.
        
        '''
        try:
            # Drop level_0, first_name, last_name, 1 column 
            input_df = input_df.drop(['level_0','first_name','last_name','1'], axis=1)

            # Resetting index
            input_df.reset_index(drop=True, inplace=True)

            return input_df

        except Exception as error_details:
            print(f"Error cleaning order data table: {str(error_details)}") 

    def clean_date_time_data(self, input_df):
        '''
        
        This function is used clean date time data for the date times table.
        Returns:
            return input_df = Cleaned data frame.
            Exception = returns error code if the function fails.
        
        '''
        try:

            # Replace NULL with na
            input_df.replace('NULL', np.nan, inplace= True)

            # Drop rows with missing values
            input_df.dropna(inplace=True)

            # Cleaning erroneous data by removing month rows longer than 4.
            input_df = input_df[input_df['month'].str.len() <= 4]

            return input_df

        except Exception as error_details:
            print(f"Error cleaning date time data: {str(error_details)}")
