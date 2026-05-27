from pydantic import ConfigDict, BaseModel

class CustomerBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


