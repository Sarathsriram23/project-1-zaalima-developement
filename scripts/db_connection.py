import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default connection parameters (can be overridden via environment variables)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "customer_churn_db")

# Construct PostgreSQL URL
POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLITE_URL = "sqlite:///customer_churn_db.sqlite"

def get_engine():
    """
    Attempts to connect to PostgreSQL database. 
    Falls back to local SQLite database if PostgreSQL connection fails.
    """
    try:
        # Try connecting to PostgreSQL
        logger.info(f"Attempting to connect to PostgreSQL at {DB_HOST}:{DB_PORT}...")
        engine = create_engine(POSTGRES_URL)
        # Test connection
        with engine.connect() as conn:
            logger.info("Successfully connected to PostgreSQL database.")
            return engine
    except Exception as e:
        logger.warning(
            f"Failed to connect to PostgreSQL (Error: {e}).\n"
            "Falling back to local SQLite database 'customer_churn_db.sqlite' for local run..."
        )
        engine = create_engine(SQLITE_URL)
        return engine

if __name__ == "__main__":
    engine = get_engine()
    print("Database Engine created:", engine)
