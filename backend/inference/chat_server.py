from fastapi import FastAPI
from pydantic import BaseModel
from .model_manager import model_manager


app = FastAPI()

# Input JSON from editor
class ChatRequest(BaseModel):
    message: str

# Output JSON to editor
class ChatResponse(BaseModel):
    reply: str
    status: str = "ok"

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = model_manager.generate_reply(req.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        return ChatResponse(reply=str(e), status="error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.inference.chat_server:app", host="127.0.0.1", port=5000, reload=True)
