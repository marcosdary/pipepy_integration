from pydantic import ConfigDict, BaseModel

class PipefyFieldBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

