import tabula
import pandas as pd
import requests
import boto3


class DataExtractor:
    '''
        This class is used to store methods for extracting data for all sources related to this project.

        Attributes:
            
            header (dict): A key-value pair of the api key to access store details
        
    '''
    def __init__(self):
       
        self.header = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        

    def read_rds_table(self, db_connector_ins, table_name):
        '''
        
        This function is used to read the rds tables from db_connector_ins and check if a specified table_name is within the list. If the table_name is in the list then the table is extracted into a Pandas DataFrame.
        If table_name is not found then the function returns an exception and prints the error.

        Returns:
            extracted_df = Data that has been extracted from the specified table_name in the form of a Pandas DataFrame.
            Exception = returns error code if the function fails.
        
        '''
        try:
            tables = db_connector_ins.list_db_tables()
            print(tables)
            if tables and table_name in tables:
                engine = db_connector_ins.init_db_engine()
                if engine:
                    extracted_df = pd.read_sql_table(table_name, con=engine)
                    
                    return extracted_df
                else:
                    return None
            else:
                print(f"Table '{table_name}' does not exist.")
                return None
        except Exception as error_details:
            print(f"Error reading RDS table into DataFrame: {str(error_details)}")
            return None
        
    def retrieve_pdf_data(self, link):
        '''
       
        This function retrieves pdf data from the input link and outputs a Pandas DataFrame containing complete pdf data.
        This uses the tabula module and is optimized for multiple pages and pdf table with defined lines between data
        This function returns an error code if Exception occurs and the function fails.


        Returns:
            pdf_df = Data that has been extracted from the pdf in the specified link in the form of a Pandas DataFrame.
            Exception = returns error code if the function fails.

        '''
        try:
            # Retrieve list of dfs in pdf file
            pdf_df_list =  tabula.read_pdf(link, pages="all", multiple_tables=True ,stream=False)
            # Concatenate all dfs into one main pandas df
            pdf_df = pd.concat(pdf_df_list, ignore_index=True)
            return pdf_df
        except Exception as error_details:
            print(f"Error reading pdf tables into DataFrame: {str(error_details)}")
            return None
        
    def list_number_of_stores(self, endpoint, header):
        '''
        
        This function accesses the site from the given endpoint and header to extract number of stores in the access point.


        Returns:
            response = returns the response from the request in the form of a json file
            Exception = returns error code if the function fails.

        '''
        try:
            response = requests.get(endpoint, headers=header)
            response.raise_for_status()
            return response.json()
        
        except Exception as error_details:
            print(f"Error obtaining list of number of stores in access point: {str(error_details)}")
            return None

    def retrieve_stores_data(self, base_endpoint):

        '''
        This function accesses the store data located in the base_endpoint and iterates through store number obtained in list_number_of_stores function 
        to obtain data of stores with each store being a dict and appended to a list named stores_data. The list of dictionaries are then
        converted into a Pandas DataFrame.


        Returns:
            stores_df = Data that has been extracted from the base endpoint in the form of a Pandas DataFrame.
            Exception = returns error code if the function fails.

        '''
        # Initialize list of dict to store store data
        stores_data = []
        try: 
        # Iterating through all 452 stores
            for store_number in range(0, 451):
                    endpoint = f"{base_endpoint}/store_details/{store_number}"
                    response = requests.get(endpoint, headers=self.header)
                    response.raise_for_status()

                    # Adding store data to list
                    stores_data.append(response.json())
        
            # Convert list of dictionaries to pandas dataframe
            stores_df = pd.DataFrame(stores_data)
            return stores_df

        except Exception as error_details:
            print(f"Error extracting store data: {str(error_details)}")
            return None

    def extract_from_s3(self, address):
        '''
        
        This function extracts data from the given s3 address into a temporary csv file which is then converted into a Pandas DataFrame.

        Returns:
            df = Data that has been extracted from the file in the specified s3 address in the form of a Pandas DataFrame.
            Exception = returns error code if the function fails.

        '''
        # Retrieve bucket and object key from the address
        s3_path_parts = address.replace("s3://","").split("/")
        bucket = s3_path_parts[0]
        key = "/".join(s3_path_parts[1:])
        
        #initializing boto s3 client
        s3 = boto3.client('s3')

        try:
            # Use a temporary file to hold data
            with open('temp.csv','wb') as temp_file:
                s3.download_fileobj(bucket,key,temp_file)

            # Read downloaded content into a Pandas DataFrame
            df = pd.read_csv('temp.csv')
            return df
        
        except Exception as error_details:
            print(f"Error extracting from S3: {str(error_details)}")
            return None




    


