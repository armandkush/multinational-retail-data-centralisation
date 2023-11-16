import tabula
import pandas as pd
import sqlalchemy
import requests
import boto3
import phonenumbers
import database_utils 



class DataExtractor:

    def __init__(self):
        self.db_connector = None
        self.engine = None
        self.tables = None
        self.user_data = None
        self.header = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        

    def read_rds_table(self, db_connector_ins, table_name):
        try:
            self.tables = db_connector_ins.list_db_tables()
            print(self.tables)
            if self.tables and table_name in self.tables:
                self.engine = db_connector_ins.init_db_engine()
                if self.engine:
                    self.user_data = pd.read_sql_table(table_name, con=self.engine)
                    
                    return self.user_data
                else:
                    return None
            else:
                print(f"Table '{table_name}' does not exist.")
                return None
        except Exception as e:
            print(f"Error reading RDS table into DataFrame: {str(e)}")
            return None
        
    def retrieve_pdf_data(self, link):
        try:
            # Retrieve list of dfs in pdf file
            pdf_df_list =  tabula.read_pdf(link, pages="all", multiple_tables=True ,stream=True)
            # Concatenate all dfs into one main pandas df
            pdf_df = pd.concat(pdf_df_list, ignore_index=True)
            return pdf_df
        except:
            return None
        
    def list_number_of_stores(self, endpoint, header):
        try:
            response = requests.get(endpoint, headers=header)
            response.raise_for_status()
            return response.json()
        
        except:
            return None

    def retrieve_stores_data(self, base_endpoint):
        # Initialize list of dict to store store data
        stores_data = []

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
    
    def extract_from_s3(self, address):
        # Retrieve bucket and object key from the address
        s3_path_parts = address.replace("s3://","").split("/")
        bucket = s3_path_parts[0]
        key = "/".join(s3_path_parts[1:])
        
        #initializing boto s3 client
        s3 = boto3.client('s3')

        try:
            # Use a temporary file to hold data
            with open('temp.csv','wb') as f:
                s3.download_fileobj(bucket,key,f)

            # Read downloaded content into a Pandas DataFrame
            df = pd.read_csv('temp.csv')
            return df
        
        except Exception as e:
            print(f"Error extracting from S3: {str(e)}")
            return None




    


