from app.errors.base import BaseError


class EmptyFieldError(BaseError):

    text = "The text cannot be empty."
    status = 400
