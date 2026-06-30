import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Connection parameters with environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "customer_churn_db")

POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Resolve the absolute path of the sqlite database relative to this script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_path = os.path.abspath(os.path.join(current_dir, "..", "customer_churn_db.sqlite")).replace("\\", "/")
SQLITE_URL = f"sqlite:///{sqlite_path}"

# Establish Engine with Fallback
try:
    logger.info("Attempting to connect API backend to PostgreSQL...")
    engine = create_engine(POSTGRES_URL, connect_args={"connect_timeout": 3})
    # Test connection
    with engine.connect() as conn:
        logger.info("Successfully connected API to PostgreSQL database.")
except Exception as e:
    logger.warning(
        f"PostgreSQL connection failed: {e}.\n"
        f"API falling back to local SQLite database: {sqlite_path}"
    )
    engine = create_engine(SQLITE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Database session generator to be used in FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_customer_data_df(query_table="telco_customers"):
    """
    Fetches raw or cleaned customer data as a Pandas DataFrame.
    """
    query = f"SELECT * FROM {query_table}"
    try:
        df = pd.read_sql(query, engine)
        logger.info(f"Successfully fetched {df.shape[0]} records from '{query_table}' table.")
        return df
    except Exception as e:
        logger.error(f"Error fetching data from table '{query_table}': {e}")
        return None

if __name__ == "__main__":
    # Test execution
    print("Testing API database connection...")
    df = fetch_customer_data_df()
    if df is not None:
        print("Success! Head of fetched records:")
        print(df.head(2))
    else:
        print("Failed to fetch customer data.")
