import io, os
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .classifier import load_or_train, predict
from .nlp import detect_intents
from .responder import build_reply
from .llm_client import classify_and_reply_openai
import logging
import re

RE_GREET = re.compile(
    r"\b(olá|oi|bom dia|boa tarde|boa noite|parabéns|parabens|feliz|boas festas|obrigado|obrigada|agradeço|agradeco|gratid[aã]o)\b",
    re.I,
)


RE_ACTION = re.compile(
    r"\b(status|atualiza(?:ção|r)?|suporte|erro|falha|problema|chamado|ticket|pedido|compra|ordem|solicita(?:ção|r)?|boleto|fatura|nota(?:\s|-)?fiscal|pagamento|prazo|anexo|documento|proposta|ajuda|acesso|senha|libera(?:r|ção)|cancelar|reativar)\b",
    re.I,
)

RE_NONSENSE = re.compile(r"^(teste+|asdf+|qwerty+|\w{1,3})$", re.I)

def is_nonsense(text: str) -> bool:
    t = (text or "").strip().lower()

    if len(t) < 8:
        return True

    words = [w for w in re.split(r"\W+", t) if w]

    if len(words) <= 2 and not RE_ACTION.search(t):
        return True

    if not ("?" in t or RE_ACTION.search(t)):
        return True
    return False

def is_non_action_message(text: str) -> bool:
    t = (text or "").strip().lower()
    return bool(RE_GREET.search(t))

def has_action_signals(text: str) -> bool:
    t = (text or "").strip().lower()
    return ("?" in t) or bool(RE_ACTION.search(t))

try:
    import pypdf
except Exception:
    pypdf = None


class PredictOut(BaseModel):
    category: str
    confidence: float
    reply: str
    provider: str
    intents: List[str]

class PredictIn(BaseModel):
    text: str


app = FastAPI(title="Projeto Email API", version="1.1.0")
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_methods=["*"],
    allow_headers=["*"],
)


CLF = load_or_train()


def read_pdf(file_bytes: bytes) -> str:
    if not pypdf:
        return ""
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        return "\n".join([p.extract_text() or "" for p in reader.pages]).strip()
    except Exception:
        return ""

def run_pipeline(raw: str) -> PredictOut:

    if is_non_action_message(raw) and not has_action_signals(raw):
        intents = detect_intents(raw)
        return PredictOut(
            category="Improdutivo",
            confidence=0.99,
            reply="Obrigado pela mensagem! Estamos à disposição.",
            provider="rule",
            intents=intents,
        )
    if is_nonsense(raw):
        intents = detect_intents(raw)
        return PredictOut(
            category="Improdutivo",
            confidence=0.99,
            reply="Mensagem recebida, mas não identificamos um pedido claro.",
            provider="rule",
            intents=intents,
        )
    
    use_llm = os.getenv("AI_PROVIDER", "none").strip().lower() == "openai"
    intents = detect_intents(raw)

    if use_llm:
        llm = classify_and_reply_openai(raw)
        logging.getLogger("uvicorn.error").info(f"LLM response: {llm}")
        if llm.get("enabled"):
            cat = llm.get("category") or "Produtivo"
            rep = (llm.get("reply") or "").strip()
            
            if not rep:
                rep = build_reply(cat, raw, intents)
            return PredictOut(
                category=cat,
                confidence=0.95,   
                reply=rep,
                provider="openai",
                intents=intents,
            )
        

    
    label, conf = predict(CLF, raw)
    reply = build_reply(label, raw, intents)
    return PredictOut(
        category=label,
        confidence=conf,
        reply=reply,
        provider="baseline",
        intents=intents,
    )


@app.get("/")
def health():
    return {"ok": True}

@app.post("/api/predict-text", response_model=PredictOut)
async def api_predict_text(payload: PredictIn):
    raw = (payload.text or "").strip()
    if not raw:
        return JSONResponse({"error": "Nenhum texto encontrado."}, status_code=400)
    return run_pipeline(raw)

@app.post("/api/predict-file", response_model=PredictOut)
async def api_predict_file(file: UploadFile = File(...)):
    if not file or not file.filename:
        return JSONResponse({"error": "Arquivo não recebido."}, status_code=400)

    name = (file.filename or "").lower()
    content = await file.read()

    if name.endswith(".txt") or (file.content_type or "").startswith("text/"):
        raw = content.decode("utf-8", errors="ignore").strip()
    elif name.endswith(".pdf") or (file.content_type or "") == "application/pdf":
        raw = read_pdf(content)
    else:
        return JSONResponse({"error": "Formato não suportado (.txt/.pdf)."}, status_code=400)

    if not raw:
        return JSONResponse({"error": "Nenhum texto encontrado."}, status_code=400)

    if len(raw.split()) > 5:
        raw = f"Segue um documento em anexo:\n\n{raw}"

    return run_pipeline(raw)
