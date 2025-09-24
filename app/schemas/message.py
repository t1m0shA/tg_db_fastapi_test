from pydantic import BaseModel, Field


class Message(BaseModel):

    id: int = Field(..., gt=0)
    text: str
    bio: str
