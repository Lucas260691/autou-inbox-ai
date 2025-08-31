import re
from typing import List

PT_STOP = {"a","à","ao","aos","as","às","de","do","dos","da","das","para","por","com","sem","sob","sobre","entre",
"e","ou","mas","também","que","quem","quando","onde","como","qual","quais","se","já","não","sim","há","na","no","nos","nas",
"num","numa","numas","numos","pra","pro","pros","pras","em","uma","umas","uns","um","ser","estar","ter","haver","foi","era",
"são","é","seja","tem","têm","tenho","meu","minha","meus","minhas","seu","sua","seus","suas","nosso","nossa","nossos",
"nossas","dele","dela","deles","delas","o","os","vou","vai","vamos","vão","ir","lá","aqui","aí","ali","bom","boa","dia","ola","olá"}
EN_STOP = {"a","an","the","this","that","these","those","and","or","but","if","in","on","at","by","for","with","about","against",
"between","into","through","during","before","after","above","below","to","from","up","down","out","off","over","under","again","further",
"then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor",
"not","only","own","same","so","than","too","very","can","will","just","don","should","now","is","are","was","were","be","been","being",
"have","has","had","having","do","does","did","doing"}

def clean_text(s: str) -> str:
    if not s: return ""
    s = s.replace("\x00", " ")
    s = re.sub(r"(?im)^>.*$", "", s)                
    s = re.sub(r"(?is)\n--\s*\n.*$", "", s)         
    s = re.sub(r"(?is)\nDe:.*?\nEnviado:.*?(?=\n\n|\Z)", "", s)  
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def tokenize(s: str) -> List[str]:
    return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9@._-]+", s.lower())

def remove_stopwords(tokens: List[str]) -> List[str]:
    stop = PT_STOP | EN_STOP
    return [t for t in tokens if t not in stop and len(t) > 1]

def preprocess(s: str) -> str:
    s = clean_text(s)
    toks = tokenize(s)
    toks = remove_stopwords(toks)
    return " ".join(toks)

def detect_language(s: str) -> str:
    pt = sum(1 for w in ["por favor","obrigado","pedido","fatura","boleto","anexo","atualiza","status","retorno","chamado"] if w in (s or "").lower())
    en = sum(1 for w in ["please","thanks","invoice","attachment","status","update","request","ticket","support"] if w in (s or "").lower())
    return "pt" if pt >= en else "en"

_INTENTS = {
    "status": re.compile(r"\b(status|atualiza|andamento|update|follow\s*up)\b", re.I),
    "attachment": re.compile(r"\b(anexo|attachment|attached)\b", re.I),
    "support": re.compile(r"\b(erro|error|bug|falha|acesso|login|crash|issue)\b", re.I),
    "billing": re.compile(r"\b(fatura|boleto|invoice|pagamento|payment|cobran[çc]a)\b", re.I),
}
def detect_intents(s: str) -> List[str]:
    return [k for k,rx in _INTENTS.items() if rx.search(s or "")]
