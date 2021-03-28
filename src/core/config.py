from os.path import dirname, join

from pydantic import BaseSettings

class Settings(BaseSettings):
    # slack
    SLACK_TOKEN: str
    SLACK_CHANNEL: str
    # aws
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    REGION_NAME: str
    AVAILABILITY_ZONE: str

    AMI_ID: str
    SECURITY_GROUP_ID: str

    class Config:
        env_file = join(dirname(__file__), "../../.env")
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
