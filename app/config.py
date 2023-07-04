from pydantic import BaseSettings

class Settings(BaseSettings):

    main_database: str
    database_host: str
    database_port: str
    database_name: str = 'project_api' 
    database_username: str = 'postgres'
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:

        env_file = '.env'

settings = Settings()