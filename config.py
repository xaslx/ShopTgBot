from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config:

    TOKEN_BOT: str = os.getenv('TOKEN_BOT')

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"




env_config: Config = Config()