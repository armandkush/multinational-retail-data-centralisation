import pandas as pd

class DataCleaning:
    def __init__(self):
        pass

    def clean_user_data(self, user_data_df):
        try:
            # Drop rows with missing values
            user_data_df.dropna(subset=['column_name'],inplace=True)

            # Clean date columns (get correct date columns name)
            user_data_df['date'] = pd.to_datetime(user_data.df['date'], errors='coerce')
            user_data_df = user_data_df.dropna(subset=['date'])

            # Handle incorrectly typed values (get correct column)
            user_data_df['column'] = pd.to_numeric(user_data_df['column'], errors='coerce')
            user_data_df = user_data_df.dropna(subset=['column'])

            # Return the cleaned DataFrame
            return user_data_df
        
        except Exception as e:
            print(f"Error cleaning user data: {str(e)}")
            return None
        