import os

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.2"))


def build_llm(temperature: float = GROQ_TEMPERATURE) -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env before starting the server."
        )
    return ChatGroq(model=GROQ_MODEL, temperature=temperature, api_key=api_key)


def health_check() -> dict:
    try:
        llm = build_llm()
        reply = llm.invoke("Reply with the single word: ok")
        text = (reply.content or "").strip().lower()
        healthy = "ok" in text
        return {
            "healthy": healthy,
            "model": GROQ_MODEL,
            "detail": "Model reachable." if healthy else f"Unexpected reply: {text!r}",
        }
    except Exception as exc:
        return {
            "healthy": False,
            "model": GROQ_MODEL,
            "detail": f"{type(exc).__name__}: {exc}",
        }
