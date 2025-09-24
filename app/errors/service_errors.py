from app.errors.base import BaseError


class ClassifierNotConfiguredError(BaseError):

    text = "The classifier is missing configuration or implementation."
    status = 500


class ClassifierConnectionError(BaseError):

    text = "Classifier connection error occurred."
    status = 503


class ClassificationFailedError(BaseError):

    text = "Unexpected classifier error occurred."
    status = 500
