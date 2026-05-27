from pydantic import BaseModel

class IndexSchema(BaseModel):
    version: str
    message: str


