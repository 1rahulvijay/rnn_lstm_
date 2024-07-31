from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    env: str = Field('dev', env='ENV')  # Environment: dev, uat, prod
    execution_context: str = Field('server', env='EXEC_CONTEXT')  # Execution context: server, airflow

    _base_path: str = None
    _credentials: dict = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def base_path(self):
        if self._base_path is None:
            self._base_path = r'\im\folder' if self.execution_context == 'airflow' else r'\airflow\sonic\im\folder'
        return self._base_path

    @base_path.setter
    def base_path(self, value: str):
        self._base_path = value

    @property
    def credentials(self):
        if self._credentials is None:
            credentials_map = {
                'prod': {'user': 'prod_user', 'password': 'prod_password'},
                'uat': {'user': 'uat_user', 'password': 'uat_password'},
                'dev': {'user': 'dev_user', 'password': 'dev_password'}
            }
            self._credentials = credentials_map.get(self.env, credentials_map['dev'])
        return self._credentials

    @credentials.setter
    def credentials(self, value: dict):
        self._credentials = value

# Usage
settings = Settings()

# Accessing the properties
base_path = settings.base_path
credentials = settings.credentials

# Example usage
print(f"Base path: {base_path}")
print(f"Credentials: User - {credentials['user']}, Password - {credentials['password']}")

# Dynamically updating the properties
settings.base_path = r'\new\base\path'
settings.credentials = {'user': 'new_user', 'password': 'new_password'}

# Verifying the updates
print(f"Updated base path: {settings.base_path}")
print(f"Updated credentials: User - {settings.credentials['user']}, Password - {settings.credentials['password']}")
