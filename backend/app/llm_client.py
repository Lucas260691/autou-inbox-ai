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
        "Você é um triador de e-mails corporativos. Classifique e gere uma resposta curta e educada.\n"
    "Categorias possíveis (escolha uma):\n"
    "- Produtivo: requer ação/resposta específica (ex.: pedir status, suporte, dúvida sobre sistema, cobrança, envio de dados).\n"
    "- Improdutivo: não requer ação imediata (ex.: felicitações, agradecimentos, saudações, mensagens sazonais, sem pedido).\n\n"
    "Regras:\n"
    "1) Se for apenas felicitação, parabéns, obrigado(a), bom dia/boa tarde/boa noite, votos de boas festas, etc., sem pedido -> 'Improdutivo'.\n"
    "2) Se houver pergunta, pedido de status/atualização, erro, suporte, cobrança, documentação -> 'Produtivo'.\n"
    "3) Responda no mesmo idioma do e-mail (PT/EN). Seja breve e útil.\n"
    "4) Saída deve ser **somente** um JSON válido, sem comentários/markdown, no formato:\n"
    "{\"category\":\"Produtivo\" ou \"Improdutivo\",\"reply\":\"<resposta curta>\"}\n\n"
    "Exemplos:\n"
    "Email: \"Feliz aniversário!\"\n"
    "=> {\"category\":\"Improdutivo\",\"reply\":\"Muito obrigado pelos votos! 😊\"}\n"
    "Email: \"Olá, podem informar o status do chamado #123?\"\n"
    "=> {\"category\":\"Produtivo\",\"reply\":\"Olá! Estamos verificando o status do chamado #123 e retornaremos em breve.\"}\n"
    "Email: \"Obrigado!\"\n"
    "=> {\"category\":\"Improdutivo\",\"reply\":\"Nós que agradecemos! Estamos à disposição.\"}\n"
    "Email: 'Preciso do número do meu pedido.'\n"
    "=> {\"category\":\"Produtivo\",\"reply\":\"Olá! O número do seu pedido será encaminhado. Pode confirmar o CPF/CNPJ para localizar?\"}\n"
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
