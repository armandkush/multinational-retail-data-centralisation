import yaml
import pandas as pd
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine

class DatabaseConnector:
    
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def read_db_creds(self, yaml_file):
        try:
            with open(yaml_file, 'r') as cred:
                credentials = yaml.safe_load(cred)
            return credentials
        except Exception as e:
            print(f"Error reading database credentials: {str(e)}")
            return None
    
    def init_db_engine(self, cred_file):

        creds = self.read_db_creds(cred_file)

        if creds:
            try:
                db_url = f"postgresql://{creds['db_user']}:{creds['db_password']}@{creds['db_host']}/{creds['db_name']}"

                engine = create_engine(db_url)
                return engine
            except Exception as e:
                print(f"Error initializing database engine: {str(e)}")
                return None
        else:
            print("Unable to intialize database engine due to missing or invalid credentials. ")
            return None


    def list_db_tables(self):
        try:
            table_names = self.engine.table_names()
            return table_names
        except Exception as e:
            print(f"Error listing database tables: {str(e)}")
            return None
    
    def upload_to_db(self, df, table_name):
        try: 
        # Upload the DataFrame to the specific table
            df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
            print(f"Data uploaded to table '{table_name}' successfully. ")

        except Exception as e:
            print(f"Error uploading data to the database: {str(e)}")
