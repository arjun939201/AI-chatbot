from fastapi import APIRouter
from pydantic import BaseModel
from chat_history import append_message, load_history, clear_history

router = APIRouter()


# ==========================================
# MODELS
# ==========================================

class ChatRequest(BaseModel):
    message: str


# ==========================================
# BOT LOGIC
# ==========================================

def generate_bot_reply(user_message: str) -> str:
    normalized = user_message.strip().lower()
    if not normalized:
        return "దయచేసి నాకు సమాధానం చెప్పడానికి ఏదో టైప్ చేయండి."
    if "hello" in normalized or "hi" in normalized or "హలో" in normalized or "ఓపి" in normalized or "వైరా" in normalized:
        return "హలో! నేను మీ TelAI తెలుగు చాట్ సహాయకుణం. నేను ఎలా సహాయం చేయగలను?"
    if "help" in normalized or "సహాయం" in normalized or "సహాయం కావాలి" in normalized:
        return "నేను మీ సంభాషణను గుర్తుంచుకోగలను మరియు సాధారణ ప్రశ్నలకు సమాధానం చెప్పగలను."
    if "name" in normalized or "పేరు" in normalized:
        return "నేను FastAPIతో నిర్మించిన ఒక సాధారణ తెలుగు చాట్ సహాయకుణం."
    if "time" in normalized or "సమయం" in normalized:
        return "నాకు నిజమైన గడియారం లేదు, కానీ నేను మీ చాట్ చరిత్రను జాగ్రత్తగా నిల్వ చేయగలను."
    return "ఆ విషయం ఆసక్తికరంగా ఉంది. మరింత చెప్పండి, నేను సహాయం చేయగలను."


# ==========================================
# ROUTES
# ==========================================

@router.post("/")
async def chat(payload: ChatRequest):
    """Send a message and get a bot reply."""
    append_message("user", payload.message)
    reply = generate_bot_reply(payload.message)
    append_message("bot", reply)
    return {"reply": reply, "history": load_history()}


@router.post("/clear")
async def clear():
    """Clear the full chat history."""
    return {"history": clear_history()}


@router.get("/history")
async def history():
    """Return the current chat history."""
    return {"history": load_history()}
