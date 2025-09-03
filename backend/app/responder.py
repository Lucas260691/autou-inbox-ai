from typing import List
from .nlp import detect_language

def build_reply(category: str, text: str, intents: List[str]) -> str:
    lang = detect_language(text or "")
    if category == "Improdutivo":
        return ("Obrigado pela mensagem! Registramos seu contato. "
                "Se precisar de suporte ou tiver uma solicitação, responda com detalhes "
                "(nº do pedido/chamado e contexto).") if lang=="pt" else (
                "Thanks for your message! We've recorded your note. "
                "If you need support or have a request, please reply with details "
                "(order/ticket number and context).")
    parts = ["Olá! Obrigado pelo contato. "] if lang=="pt" else ["Hello! Thanks for reaching out. "]
    if "status" in intents:
        parts += ["Estamos verificando o status e retornaremos em breve. ",
                  "Confirme o nº do chamado/pedido. "] if lang=="pt" else \
                 ["We're checking your request status and will get back shortly. ",
                  "Please confirm the ticket/order number. "]
    if "attachment" in intents:
        parts += ["Recebemos o(s) anexo(s) e encaminhamos para validação. "] if lang=="pt" else \
                 ["We received the attachment(s) and sent them for validation. "]
    if "support" in intents:
        parts += ["Para avançarmos, envie passos de reprodução, prints e horário aproximado do ocorrido. "] if lang=="pt" else \
                 ["To proceed, share reproduction steps, screenshots, and approximate time. "]
    if "billing" in intents:
        parts += ["Encaminhamos ao financeiro; inclua CNPJ, nº da NF e valor esperado. "] if lang=="pt" else \
                 ["Forwarded to billing; include VAT/CNPJ, invoice number, expected amount. "]
    if not intents:
        parts += ["Nossa equipe está tratando seu pedido e responderá com próximos passos. "] if lang=="pt" else \
                 ["Our team is handling your request and will reply with next steps. "]
    parts += ["Ficamos à disposição."] if lang=="pt" else ["We're at your disposal."]
    return "".join(parts)
