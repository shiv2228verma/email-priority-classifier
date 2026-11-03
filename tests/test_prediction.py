import pandas as pd
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from prediction import predict_emails

@pytest.fixture
def small_model():
    texts = ["server outage production down urgent", "security breach respond immediately",
             "weekly team meeting schedule", "monthly project progress update",
             "optional newsletter read later", "holiday greeting no action"]
    labels = ["Urgent", "Urgent", "Normal", "Normal", "Low", "Low"]
    model = Pipeline([("tfidf", TfidfVectorizer()), ("classifier", LogisticRegression(max_iter=500))])
    model.fit(texts, labels)
    return model

def test_prediction_adds_label_confidence_and_explanation(small_model):
    frame = pd.DataFrame([{"subject": "Production server outage", "body": "The service is down. Respond immediately."}])
    result = predict_emails(frame, small_model)
    assert result.loc[0, "predicted_priority"] in {"Urgent", "Normal", "Low"}
    assert 0 <= result.loc[0, "confidence"] <= 100
    assert "explanation_terms" in result.columns

def test_prediction_rejects_missing_columns(small_model):
    with pytest.raises(ValueError, match="Missing required"):
        predict_emails(pd.DataFrame({"subject": ["Hello"]}), small_model)
