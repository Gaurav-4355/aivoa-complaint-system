import json
from fastapi import APIRouter
from app.agents.nodes import _call_groq
from app.agents import prompts
from app.config import settings
from app import schemas

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=schemas.ChatResponse)
def ask_assistant(payload: schemas.ChatRequest):
    """
    Powers the 'Ask me anything about this complaint...' chat box.
    Grounds the answer in whatever fields have been extracted so far.
    """
    context = payload.context.model_dump() if payload.context else {}
    system = prompts.CHAT_SYSTEM_PROMPT.format(context_json=json.dumps(context))
    full_prompt = f"{system}\n\nUser question: {payload.question}"
    answer = _call_groq(full_prompt, settings.GROQ_REASONING_MODEL)
    return schemas.ChatResponse(answer=answer.strip())
