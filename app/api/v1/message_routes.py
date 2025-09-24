from fastapi import APIRouter

router = APIRouter()


@router.get("/classify_message")
def classify_message_handler():

    is_lead = False
    return {"lead": is_lead}
