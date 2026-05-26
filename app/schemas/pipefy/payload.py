from pydantic import ConfigDict, BaseModel, Field
from typing import Annotated, Optional

from app.schemas.pipefy.card.read import PipefyCardReadSchema

class PipefyPayloadSchema(BaseModel):
    card: Annotated[Optional[PipefyCardReadSchema], Field(default=None)]
    success: Annotated[Optional[bool], Field(default=False)]
     
    model_config = ConfigDict(from_attributes=True)


