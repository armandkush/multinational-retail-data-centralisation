import sqlalchemy
import pandas as pd


class DataExtractor:

    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    def extract_data_from_db(self, table_name):
        try:
        # connect to the database using the engine

            engine = self.db_connector.engine
            conn = engine.connect()
        

        #Query data from specific table

            query = f"SELECT * FROM {table_name}"
            result = conn.execute(query)

        # Fetch and return the data
            data = result.fetchall()
            return data
        
        except Exception as e:
            print(f"Error extracting data from the database: {str(e)}")
            return None
    

    def read_rds_table(self, table_name):
        try:
            # connect to databse using engine
            engine = self.db_connector.engine
            conn = engine.connect()
            
            #query data from the specific table and convert to dataframe
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            
            #close the database connection
            conn.close()

            return df
        except Exception as e:
            print(f"Error reading RDS table into DataFrame: {str(e)}")
            return None

    


