import os, json, pathlib
from typing import Tuple
from joblib import dump, load
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .nlp import preprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEED_PATH = os.getenv("SEED_DATA_PATH", str(ROOT / "data" / "seed.jsonl"))
MODEL_PATH = os.getenv("MODEL_PATH", str(ROOT / "model" / "baseline.joblib"))

def load_seed_dataset():
    data = []
    if os.path.exists(SEED_PATH):
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try: data.append(json.loads(line))
                except: pass
    if not data:
        data = [
            {"text":"Poderiam informar o status do chamado #12345 ainda hoje?", "label":"Produtivo"},
            {"text":"Feliz Natal a todos! Obrigado pelo suporte.", "label":"Improdutivo"},
            {"text":"Segue anexo a nota fiscal. Podem confirmar o recebimento?", "label":"Produtivo"},
            {"text":"Bom dia, apenas agradecendo o atendimento de ontem.", "label":"Improdutivo"},
            {"text":"Please update ticket #998; login error. Screenshot attached.", "label":"Produtivo"},
            {"text":"Thank you for your help last week!", "label":"Improdutivo"},
        ]
    X = [preprocess(d["text"]) for d in data]
    y = [d["label"] for d in data]
    return X, y

def train_and_save(path_model: str = MODEL_PATH) -> Pipeline:
    X, y = load_seed_dataset()
    clf = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("lr", LogisticRegression(max_iter=1000))
    ])
    clf.fit(X, y)
    pathlib.Path(path_model).parent.mkdir(parents=True, exist_ok=True)
    dump(clf, path_model)
    return clf

def load_or_train() -> Pipeline:
    if os.path.exists(MODEL_PATH):
        try: return load(MODEL_PATH)
        except: pass
    return train_and_save()

def predict(clf: Pipeline, text: str) -> Tuple[str, float]:
    proba = clf.predict_proba([preprocess(text)])[0]
    classes = list(clf.classes_)
    idx = int(proba.argmax())
    return classes[idx], float(proba[idx])
