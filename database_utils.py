import yaml
import sqlalchemy
from sqlalchemy import inspect


class DatabaseConnector:
    '''
        This class is used to establish connection with the postgres RDS postgres database in this project.

        Attributes:
            
            self.creds_file (dict): A key-value pair of the api key to access store details
        
    '''
    def __init__(self, creds_file):
       self.creds_file = creds_file

    def read_db_creds(self):
        '''
        
        This function is used to read the creds_file and return a yaml file containing the credentials

        Returns:
            credentials = Credentials data that has been extracted from the specified creds_file in the form of a yaml file.
            Exception = returns error code if the function fails.
        
        '''
        try:
            with open(self.creds_file, 'r') as file:
                credentials = yaml.safe_load(file)
            return credentials
        except Exception as error_details:
            print(f"Error reading database credentials: {str(error_details)}")
            return None
    
    def init_db_engine(self):
        '''
        
        This function is used to initialise the database engine for connection
        Returns:
            engine = sqlalchemy engine instance to connect to specified rds database.
            Exception = returns error code if the function fails.
        
        '''
        try:
            credentials = self.read_db_creds()
            if credentials:
                db_url = f"postgresql://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}"
                engine = sqlalchemy.create_engine(db_url)
                return engine
            else:
                return None
        except Exception as error_details:
            print(f"Error initializing database engine: {str(error_details)}")
            return None

    def list_db_tables(self):
            '''
        
        This function is used to inspect the rds database and list all table name found in the database

        Returns:
            table_names = list containing all table names found in rds database

            '''   
            engine = self.init_db_engine()
            if engine:
                insp = inspect(engine)
                table_names = insp.get_table_names()
                return table_names   
    
    def upload_to_db(self, df, table_name):
        '''
        
        This function is used to upload specified pandas df as table_name in the set RDS database
        
        '''
        # Credentials for local postgres server.
        username = 'postgres'
        password = '(1K3l05)'
        host = 'localhost'
        port = '5432'
        database = 'sales_data'

        # Connecting the engine.
        connection_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        engine = sqlalchemy.create_engine(connection_url)

        try: 
        # Upload the DataFrame to the specific table
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"Data uploaded to table '{table_name}' successfully. ")

        except Exception as error_details:
            print(f"Error uploading data to the database: {str(error_details)}")
