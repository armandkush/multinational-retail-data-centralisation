from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Create instances
db_connector = DatabaseConnector()
data_extractor = DataExtractor(db_connector)
data_cleaner = DataCleaning()

# Initialize database engine
engine = db_connector.init_db_engine('db_creds.yaml')

tables = db_connector.list_db_tables()
print(tables)