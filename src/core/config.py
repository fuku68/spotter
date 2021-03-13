from os.path import dirname, join

from pydantic import BaseSettings

class Settings(BaseSettings):
    SLACK_TOKEN: str

    class Config:
        env_file = join(dirname(__file__), "../../.env")
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
