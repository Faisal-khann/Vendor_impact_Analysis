import pandas as pd
from sqlalchemy import create_engine
import os
import logging
import time

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Database engine
engine = create_engine("sqlite:///inventory.db")  # or any DB you use

def ingest_csv_in_chunks(file_path, table_name, engine, chunk_size=100000):
    """
    Ingests a large CSV file into a database in chunks.

    Parameters:
        file_path (str): Path to the CSV file.
        table_name (str): Name of the target table.
        engine (SQLAlchemy Engine): SQLAlchemy database engine.
        chunk_size (int): Number of rows per chunk.

    Returns:
        None
    """
    first_chunk = True
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        if_exists_mode = 'replace' if first_chunk else 'append'
        chunk.to_sql(table_name, con=engine, if_exists=if_exists_mode, index=False)
        first_chunk = False

def load_raw_data():
    """
    Loads all CSV files from the 'data' directory and ingests them into the database.
    """
    data_dir = 'data'
    
    if not os.path.exists(data_dir):
        logging.error(f"Data directory '{data_dir}' does not exist.")
        return

    logging.info("Starting to load raw CSV files from 'data' directory.")

    start = time.time()

    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(data_dir, file)
            table_name = os.path.splitext(file)[0]

            logging.info(f"Starting chunked ingestion for file: {file}")

            try:
                ingest_csv_in_chunks(file_path, table_name, engine)
                logging.info(f"Successfully ingested file: {file} into table: {table_name}")
            except Exception as e:
                logging.error(f"Failed to ingest file: {file} — Error: {e}")

    end = time.time()
    total_time = (end - start) / 60
    logging.info("Finished loading all raw CSV files.")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")

# Main trigger
if __name__ == '__main__':
    load_raw_data()
