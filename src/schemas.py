
from pydantic import BaseModel, Field

class URL_SCHEMA(BaseModel):
    long_url:str = Field(min_length=1)
    
    