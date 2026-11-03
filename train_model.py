"""Train and evaluate the MailSense AI baseline classifier."""
from __future__ import annotations
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from preprocessing import combine_email_text

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "training_data" / "sample_training_emails.csv"
MODEL_PATH = ROOT / "artifacts" / "priority_model.joblib"
REPORT_PATH = ROOT / "artifacts" / "evaluation.json"
VALID_LABELS = {"Urgent", "Normal", "Low"}

def build_pipeline() -> Pipeline:
    """Create a lightweight TF-IDF + Logistic Regression model."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=12000, strip_accents="unicode", sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced")),
    ])

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Training data not found: {DATA_PATH}")
    frame = pd.read_csv(DATA_PATH)
    missing = {"subject", "body", "priority"}.difference(frame.columns)
    if missing:
        raise ValueError(f"Training CSV is missing columns: {', '.join(sorted(missing))}")
    frame = frame.dropna(subset=["priority"]).copy()
    frame["priority"] = frame["priority"].astype(str).str.strip().str.title()
    unknown = set(frame["priority"]) - VALID_LABELS
    if unknown:
        raise ValueError(f"Unsupported priority labels: {', '.join(sorted(unknown))}")
    frame["text"] = [combine_email_text(s, b) for s, b in zip(frame["subject"], frame["body"])]
    frame = frame[frame["text"].str.len() > 0]
    counts = frame["priority"].value_counts()
    if len(counts) != 3 or counts.min() < 2:
        raise ValueError("Training data must contain at least two examples of each class.")
    x_train, x_test, y_train, y_test = train_test_split(
        frame["text"], frame["priority"], test_size=0.25, random_state=42, stratify=frame["priority"])
    model = build_pipeline()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    report = classification_report(y_test, predictions, labels=["Urgent", "Normal", "Low"], output_dict=True, zero_division=0)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "macro_f1": round(float(report["macro avg"]["f1-score"]), 4),
        "weighted_f1": round(float(report["weighted avg"]["f1-score"]), 4),
        "train_samples": int(len(y_train)),
        "test_samples": int(len(y_test)),
        "class_order": ["Urgent", "Normal", "Low"],
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=["Urgent", "Normal", "Low"]).tolist(),
        "classification_report": report,
        "note": "Small demonstration dataset; metrics are not production evidence.",
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    REPORT_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Model saved: {MODEL_PATH.relative_to(ROOT)}")
    print(f"Hold-out accuracy: {metrics['accuracy']:.2%}")
    print(classification_report(y_test, predictions, zero_division=0))
    print(f"Evaluation saved: {REPORT_PATH.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
