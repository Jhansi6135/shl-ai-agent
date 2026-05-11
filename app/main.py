from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ai_search import search

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


def needs_clarification(messages):

    latest = messages[-1].content.lower()

    vague_phrases = [
        "need assessment",
        "need test",
        "hiring",
        "assessment",
        "test"
    ]

    if len(latest.split()) < 5:
        return True

    for phrase in vague_phrases:
        if phrase in latest and len(latest.split()) < 8:
            return True

    role_keywords = [
        "developer",
        "manager",
        "engineer",
        "analyst",
        "sales",
        "java",
        "python"
    ]

    found = any(word in latest for word in role_keywords)

    return not found


@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages

    # clarification
    if needs_clarification(messages):

        return {
            "reply": (
                "Could you share the role, "
                "experience level, and skills required?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # combine user messages
    query = " ".join(
        [m.content for m in messages if m.role == "user"]
    )

    # retrieve recommendations
    results = search(query)

    recommendations = []

    for r in results[:5]:

        recommendations.append({
            "name": r["name"],
            "url": r["link"],
            "test_type": "K"
        })

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }

# test run  uvicorn main:app --reload