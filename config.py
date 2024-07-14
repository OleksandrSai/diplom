from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_PREFIX: str = '/api'
    ZIGBEE_PAN_ID: int
    ZIGBEE_CHANEL: int
    ZIGBEE_KEY: str
    ZIGBEE_SERIAL_PORT: str

    @property
    def DATABASE_URL_pymysql(self):
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


load_dotenv()
settings = Settings()
