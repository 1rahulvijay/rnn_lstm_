import os

class Config:
    SERVER_PATH = r'\airflow\sonic\im\folder'
    AIRFLOW_PATH = r'\im\folder'
    
    def __init__(self):
        self.env = os.getenv('ENV', 'dev').lower()  # Default to 'dev' if ENV variable is not set
        self.execution_context = os.getenv('EXEC_CONTEXT', 'server').lower()  # Default to 'server' if EXEC_CONTEXT variable is not set
        self.base_path = self.AIRFLOW_PATH if self.execution_context == 'airflow' else self.SERVER_PATH
        self.credentials = self._get_credentials()

    def _get_credentials(self):
        return {
            'prod': {'user': 'prod_user', 'password': 'prod_password'},
            'uat': {'user': 'uat_user', 'password': 'uat_password'},
            'dev': {'user': 'dev_user', 'password': 'dev_password'}
        }.get(self.env, {'user': 'dev_user', 'password': 'dev_password'})

    def get_base_path(self):
        return self.base_path

    def get_credentials(self):
        return self.credentials
