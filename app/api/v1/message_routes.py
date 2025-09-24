from app.schemas import MessageDataInput
from app.services import ClassifierFactory
from fastapi import APIRouter

router = APIRouter()
classifier = ClassifierFactory.create()


@router.post("/classify_message")
async def classify_message_handler(message: MessageDataInput):

    is_lead = await classifier.classify(message.text, message.bio)
    return {"lead": is_lead}
