# backend/app/llm_client.py
import os, re, json
from typing import Dict

# redige PII (emails, CPF/CNPJ, números longos)
RE_EMAIL = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
RE_DOC   = re.compile(r"\b(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})\b")  # CPF/CNPJ simples
RE_LONG  = re.compile(r"\b\d{4,}\b")

def redact(text: str) -> str:
    if not text: return ""
    text = RE_EMAIL.sub("[email]", text)
    text = RE_DOC.sub("[doc]", text)
    text = RE_LONG.sub("[num]", text)
    return text

def _normalize_category(raw_json_value: str, fallback_source: str) -> str:
    v = (raw_json_value or "").strip().lower()
    if "produt" in v or "productive" in v:
        return "Produtivo"
    if "improdut" in v or "non-productive" in v or "improductive" in v:
        return "Improdutivo"
    # fallback simples olhando o texto bruto
    return "Produtivo" if "produt" in (fallback_source or "").lower() else "Improdutivo"

def classify_and_reply_openai(text: str) -> Dict:
    # 1) respeita AI_PROVIDER do .env (com trim)
    if os.getenv("AI_PROVIDER", "none").strip().lower() != "openai":
        return {"enabled": False, "error": "AI_PROVIDER != openai"}

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"enabled": False, "error": "OPENAI_API_KEY ausente"}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        return {"enabled": False, "error": f"SDK indisponível: {e}"}

    system = (
        "Você é um assistente de triagem de emails corporativos. "
        "Analise o email do usuário e responda APENAS um JSON válido, sem comentários ou markdown, no formato:\n"
        "{\"category\":\"Produtivo\" OU \"Improdutivo\",\"reply\":\"<resposta curta e educada no idioma do email>\"}\n"
        "Não inclua nenhum outro texto além do JSON. Garanta que 'category' seja exatamente 'Produtivo' ou 'Improdutivo'."
    )
    safe_text = redact(text or "")

    try:
        resp = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            input=[
                {"role": "system", "content": [{"type": "input_text","text": system}]},
                {"role": "user",   "content": [{"type": "input_text","text": f"Email:\n{safe_text}"}]},
            ],
            temperature=0.2,
        
        )
        raw = resp.output_text.strip()

        # normalmente já vem JSON puro
        try:
            data = json.loads(raw)
        except Exception:
            # fallback se vier com texto extra (raro com response_format=json_object)
            m = re.search(r"\{.*\}", raw, flags=re.S)
            data = json.loads(m.group(0)) if m else {}

        cat = _normalize_category(data.get("category"), raw)
        rep = (data.get("reply") or "").strip()

        return {"enabled": True, "provider": "openai", "category": cat, "reply": rep}
    except Exception as e:
        return {"enabled": False, "error": str(e)}
