from app.errors import EmptyFieldError
from pydantic import BaseModel, Field, field_validator


class MessageDataInput(BaseModel):

    text: str
    bio: str

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:

        if not v.strip():
            raise EmptyFieldError("The 'text' field cannot be empty.")

        return v

    @field_validator("bio")
    @classmethod
    def validate_bio_not_empty(cls, v: str) -> str:

        if not v.strip():
            raise EmptyFieldError("The 'bio' field cannot be empty.")

        return v
