import cx_Oracle
import pandas as pd
import logging
import time
import asyncio
import json
from typing import Optional, Dict, Any, List, Tuple
from smtplib import SMTP
from email.mime.text import MIMEText
from contextlib import contextmanager

class Config:
    def __init__(self, config: Dict[str, Any]):
        self.connection_string = config['connection_string']
        self.table_name = config['table_name']
        self.input_dataframe = config['input_dataframe']
        self.mode = config.get('mode', 'append')
        self.delete_existing_data = config.get('delete_existing_data', False)
        self.delete_condition = config.get('delete_condition', None)
        self.batch_size = config.get('batch_size', 1000)
        self.primary_key = config.get('primary_key', None)
        self.logging_level = config.get('logging_level', logging.INFO)
        self.retry_attempts = config.get('retry_attempts', 3)
        self.retry_delay = config.get('retry_delay', 5)
        self.notification_config = config.get('notification_config', None)
        self.pre_insert_sql = config.get('pre_insert_sql', None)
        self.post_insert_sql = config.get('post_insert_sql', None)
        self.async_mode = config.get('async_mode', False)
        self.json_columns = config.get('json_columns', [])
        self.clob_columns = config.get('clob_columns', [])
        self.blob_columns = config.get('blob_columns', [])

class OracleDatabaseInserter:
    def __init__(self, config: Config):
        self.config = config
        self.validate_parameters()
        self.setup_logging()
        self.connection_pool = self.create_connection_pool()

    def validate_parameters(self):
        if self.config.mode not in ['append', 'replace', 'upsert']:
            raise ValueError("Mode should be either 'append', 'replace', or 'upsert'.")
        if not isinstance(self.config.input_dataframe, pd.DataFrame):
            raise ValueError("input_dataframe should be a pandas DataFrame.")
        if not self.config.connection_string or not self.config.table_name:
            raise ValueError("Connection string and table name must be provided.")

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(self.config.logging_level)

    def create_connection_pool(self):
        return cx_Oracle.SessionPool(user="username", password="password",
                                     dsn=self.config.connection_string,
                                     min=2, max=10, increment=1, threaded=True)

    @contextmanager
    def get_connection(self):
        connection = None
        try:
            for attempt in range(self.config.retry_attempts):
                try:
                    connection = self.connection_pool.acquire()
                    yield connection
                    return
                except cx_Oracle.DatabaseError as e:
                    self.logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                    time.sleep(self.config.retry_delay)
            raise RuntimeError("All connection attempts failed.")
        finally:
            if connection:
                self.connection_pool.release(connection)

    async def insert_data(self):
        async with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                if self.config.delete_existing_data:
                    self.delete_data(cursor)

                if self.config.pre_insert_sql:
                    self.execute_custom_sql(cursor, self.config.pre_insert_sql)

                if self.config.async_mode:
                    await self.perform_insertion_async(cursor)
                else:
                    self.perform_insertion(cursor)

                if self.config.post_insert_sql:
                    self.execute_custom_sql(cursor, self.config.post_insert_sql)

                connection.commit()
                self.logger.info(f"Data successfully inserted into {self.config.table_name} using {self.config.mode} mode.")

            except cx_Oracle.DatabaseError as e:
                self.logger.error(f"Error inserting data: {str(e)}")
                connection.rollback()
                self.send_notification(f"Error inserting data: {str(e)}")
            finally:
                cursor.close()

    def delete_data(self, cursor):
        delete_query = f"DELETE FROM {self.config.table_name} "
        if self.config.delete_condition:
            delete_query += f"WHERE {self.config.delete_condition}"
            self.logger.info(f"Deleting data with condition: {self.config.delete_condition}")
        else:
            self.logger.info("Deleting all existing data from the table.")
        
        cursor.execute(delete_query)

    def perform_insertion(self, cursor):
        columns = ', '.join(self.config.input_dataframe.columns)
        placeholders = ', '.join([f":{col}" for col in self.config.input_dataframe.columns])
        insert_query = f"INSERT INTO {self.config.table_name} ({columns}) VALUES ({placeholders})"

        data_tuples = self.prepare_data_tuples()
        self.logger.info(f"Inserting data into {self.config.table_name} in batches of {self.config.batch_size}.")

        for i in range(0, len(data_tuples), self.config.batch_size):
            batch = data_tuples[i:i + self.config.batch_size]
            cursor.executemany(insert_query, batch)

    async def perform_insertion_async(self, cursor):
        columns = ', '.join(self.config.input_dataframe.columns)
        placeholders = ', '.join([f":{col}" for col in self.config.input_dataframe.columns])
        insert_query = f"INSERT INTO {self.config.table_name} ({columns}) VALUES ({placeholders})"

        data_tuples = self.prepare_data_tuples()
        self.logger.info(f"Inserting data into {self.config.table_name} in batches of {self.config.batch_size} (async).")

        for i in range(0, len(data_tuples), self.config.batch_size):
            batch = data_tuples[i:i + self.config.batch_size]
            await asyncio.sleep(0)  # Simulating async I/O operation
            cursor.executemany(insert_query, batch)

    def prepare_data_tuples(self) -> List[Tuple]:
        data_tuples = []
        for row in self.config.input_dataframe.itertuples(index=False, name=None):
            row_dict = {col: val for col, val in zip(self.config.input_dataframe.columns, row)}
            for json_col in self.config.json_columns:
                row_dict[json_col] = json.dumps(row_dict[json_col])
            for clob_col in self.config.clob_columns:
                row_dict[clob_col] = cx_Oracle.CLOB(row_dict[clob_col])
            for blob_col in self.config.blob_columns:
                row_dict[blob_col] = cx_Oracle.BLOB(row_dict[blob_col])
            data_tuples.append(tuple(row_dict.values()))
        return data_tuples

    def handle_conflicts(self, cursor):
        columns = ', '.join(self.config.input_dataframe.columns)
        placeholders = ', '.join([f":{col}" for col in self.config.input_dataframe.columns])
        update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in self.config.input_dataframe.columns if col != self.config.primary_key])
        insert_query = f"""
            MERGE INTO {self.config.table_name} t
            USING (SELECT {placeholders} FROM dual) s
            ON (t.{self.config.primary_key} = s.{self.config.primary_key})
            WHEN MATCHED THEN
                UPDATE SET {update_set}
            WHEN NOT MATCHED THEN
                INSERT ({columns})
                VALUES ({placeholders})
        """

        data_tuples = self.prepare_data_tuples()
        self.logger.info(f"Handling conflicts for primary key: {self.config.primary_key}")
        cursor.executemany(insert_query, data_tuples)

    def execute_custom_sql(self, cursor, sql_query: str):
        self.logger.info(f"Executing custom SQL: {sql_query}")
        cursor.execute(sql_query)

    def send_notification(self, message: str):
        if not self.config.notification_config:
            return

        try:
            with SMTP(self.config.notification_config['smtp_server'], self.config.notification_config['smtp_port']) as server:
                server.starttls()
                server.login(self.config.notification_config['smtp_user'], self.config.notification_config['smtp_password'])

                msg = MIMEText(message)
                msg['Subject'] = self.config.notification_config['subject']
                msg['From'] = self.config.notification_config['from']
                msg['To'] = self.config.notification_config['to']

                server.sendmail(self.config.notification_config['from'], [self.config.notification_config['to']], msg.as_string())
                self.logger.info("Notification sent successfully.")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {str(e)}")

# Example usage
if __name__ == "__main__":
    config_dict = {
        'connection_string': "username/password@hostname:port/service_name",
        'table_name': "your_table",
        'input_dataframe': pd.DataFrame({
            'column1': [1, 2, 3],
            'column2': ['A', 'B', 'C']
        }),
        'mode': 'upsert',
        'delete_existing_data': True,
        'delete_condition': "column1 > 1",
        'batch_size': 2,
        'primary_key': "column1",
        'logging_level': logging.DEBUG,
        'retry_attempts': 3,
        'retry_delay': 5,
        'notification_config': {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_user': 'user@example.com',
            'smtp_password': 'password',
            'from': 'user@example.com',
            'to': 'admin@example.com',
            'subject': 'Database Insert Error Notification'
        },
        'pre_insert_sql': "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'",
        'post_insert_sql': "COMMIT",
        'async_mode': True,
        'json_columns': ['column2'],
        'clob_columns': [],
        'blob_columns': []
    }

    config = Config(config_dict)
    inserter = OracleDatabaseInserter(config)

    if config.async_mode:
        asyncio.run(inserter.insert_data())
    else:
        inserter.insert_data()
