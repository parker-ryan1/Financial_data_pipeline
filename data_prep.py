import os
import pandas as pd
import pyodbc
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(filename='financial_pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CSVHandler(FileSystemEventHandler):
    def __init__(self, db_conn_str, column_mappings):
        self.db_conn_str = db_conn_str
        self.column_mappings = column_mappings

    def on_created(self, event):
        if event.is_directory:
            return

        file_path, file_extension = os.path.splitext(event.src_path)
        if file_extension.lower() == '.csv':
            self.process_csv(event.src_path)

    def process_csv(self, file_path):
        try:
            # Read CSV file
            df = pd.read_csv(file_path)

            # Validate financial data
            self.validate_financial_data(df)

            # Calculate growth rate
            df = self.calculate_growth_rate(df)

            # Ensure the CSV matches a column mapping
            matched = False
            for table_name, columns in self.column_mappings.items():
                if all(col in df.columns for col in columns):
                    matched = True
                    break

            if not matched:
                logging.warning(f"CSV file {file_path} does not match any required column sets.")
                return

            # Create and insert data into the appropriate table
            for table_name, columns in self.column_mappings.items():
                if all(col in df.columns for col in columns):
                    self.create_and_insert_table(table_name, columns, df[columns], file_path)

            # Archive the file
            self.archive_file(file_path)

        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")

    def validate_financial_data(self, df):
        required_columns = ['Date', 'Revenue']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV file must contain the following columns: {required_columns}")

        if not pd.api.types.is_numeric_dtype(df['Revenue']):
            raise ValueError("Revenue column must contain numeric values.")

        try:
            pd.to_datetime(df['Date'])
        except ValueError:
            raise ValueError("Date column must contain valid dates.")

    def calculate_growth_rate(self, df):
        df['Growth_Rate'] = df['Revenue'].pct_change()
        return df

    def create_and_insert_table(self, table_name, columns, data, file_path):
        conn = pyodbc.connect(self.db_conn_str)
        cursor = conn.cursor()

        columns_with_types = ", ".join([f"[{col}] NVARCHAR(100)" for col in columns])
        create_table_sql = f"""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = ?)
        BEGIN
            CREATE TABLE [{table_name}] (
                {columns_with_types}
            );
        END
        """
        cursor.execute(create_table_sql, table_name)

        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f"INSERT INTO [{table_name}] ({', '.join(['[' + col + ']' for col in columns])}) VALUES ({placeholders})"
        for _, row in data.iterrows():
            cursor.execute(insert_sql, tuple(row))

        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f"Table '{table_name}' created successfully with data from '{file_path}'")

    def archive_file(self, file_path):
        archive_folder = os.path.join(os.path.dirname(file_path), "archive")
        os.makedirs(archive_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(archive_folder, os.path.basename(file_path)))
        logging.info(f"File '{file_path}' archived to '{archive_folder}'")

# Rest of the script remains the same
