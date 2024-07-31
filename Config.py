from pydantic import BaseSettings, Field

class Config(BaseSettings):
    env: str = Field('dev', env='ENV')
    execution_context: str = Field('server', env='EXEC_CONTEXT')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def base_path(self):
        return r'\im\folder' if self.execution_context == 'airflow' else r'\airflow\sonic\im\folder'
    
    @property
    def credentials(self):
        creds = {
            'prod': {'user': 'prod_user', 'password': 'prod_password'},
            'uat': {'user': 'uat_user', 'password': 'uat_password'},
            'dev': {'user': 'dev_user', 'password': 'dev_password'}
        }
        return creds.get(self.env, creds['dev'])

# Usage
config = Config()

base_path = config.base_path
credentials = config.credentials

# Example usage
print(f"Base path: {base_path}")
print(f"Credentials: User - {credentials['user']}, Password - {credentials['password']}")

# Your script logic here, using base_path and credentials
