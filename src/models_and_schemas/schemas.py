
from pydantic import BaseModel, Field, HttpUrl

class URL_SCHEMA(BaseModel):
    long_url:HttpUrl
    
    