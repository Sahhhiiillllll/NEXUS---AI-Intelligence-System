from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class APIKeys(BaseModel):
    openrouter: str = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY"))

class JarvisConfig(BaseModel):
    api_keys: APIKeys = Field(default_factory=APIKeys)

config = JarvisConfig()
print("KEY IS:", config.api_keys.openrouter)
