import yaml
import pandas as pd
import sqlalchemy
import psycopg2
import sqlalchemy
from sqlalchemy import inspect

class DatabaseConnector:
    
    def __init__(self, creds_file):
       self.creds_file = creds_file
       self.engine = None
       self.credentials = None

    def read_db_creds(self):
        try:
            with open(self.creds_file, 'r') as file:
                credentials = yaml.safe_load(file)
            return credentials
        except Exception as e:
            print(f"Error reading database credentials: {str(e)}")
            return None
    
    def init_db_engine(self):
        try:
            self.credentials = self.read_db_creds()
            if self.credentials:
                db_url = f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
                self.engine = sqlalchemy.create_engine(db_url)
                return self.engine
            else:
                return None
        except Exception as e:
            print(f"Error initializing database engine: {str(e)}")
            return None


    def list_db_tables(self):
            engine = self.init_db_engine()
            if engine:
                insp = inspect(engine)
                table_names = insp.get_table_names()
                #print(engine.table_names())
                return  table_names
                
            
    
    def upload_to_db(self, df, table_name):
        username = 'postgres'
        password = '(1K3l05)'
        host = 'localhost'
        port = '5432'
        database = 'sales_data'

        connection_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        engine = sqlalchemy.create_engine(connection_url)

        try: 
        # Upload the DataFrame to the specific table
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"Data uploaded to table '{table_name}' successfully. ")

        except Exception as e:
            print(f"Error uploading data to the database: {str(e)}")
