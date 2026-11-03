"""Model loading and prediction helpers for MailSense AI."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import joblib
import pandas as pd
from preprocessing import combine_email_text

DEFAULT_MODEL_PATH = Path("artifacts/priority_model.joblib")

def load_model(model_path: str | Path = DEFAULT_MODEL_PATH) -> Any:
    """Load a model pipeline created by train_model.py."""
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model not found at '{path}'. Run 'python train_model.py' first.")
    return joblib.load(path)

def _explain_terms(model: Any, text: str, predicted_label: str, limit: int = 4) -> str:
    """Return high-weight terms for the predicted class when supported."""
    try:
        vectorizer = model.named_steps["tfidf"]
        classifier = model.named_steps["classifier"]
        matrix = vectorizer.transform([text])
        features = vectorizer.get_feature_names_out()
        index = list(classifier.classes_).index(predicted_label)
        contributions = matrix.toarray()[0] * classifier.coef_[index]
        ranked = contributions.argsort()[::-1]
        terms = [str(features[i]) for i in ranked if contributions[i] > 0 and matrix[0, i] > 0][:limit]
        return ", ".join(terms) if terms else "No strong positive term found"
    except (AttributeError, KeyError, ValueError, IndexError):
        return "Explanation unavailable for this model"

def predict_emails(frame: pd.DataFrame, model: Any) -> pd.DataFrame:
    """Predict priorities for a dataframe containing subject and body."""
    missing = {"subject", "body"}.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")
    result = frame.copy()
    result["subject"] = result["subject"].fillna("").astype(str)
    result["body"] = result["body"].fillna("").astype(str)
    texts = [combine_email_text(s, b) for s, b in zip(result["subject"], result["body"])]
    labels = model.predict(texts)
    probabilities = model.predict_proba(texts)
    result["predicted_priority"] = labels
    result["confidence"] = [round(float(max(row)) * 100, 2) for row in probabilities]
    result["explanation_terms"] = [_explain_terms(model, text, str(label)) for text, label in zip(texts, labels)]
    return result
