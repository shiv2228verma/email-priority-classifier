"""Streamlit interface for MailSense AI."""
from __future__ import annotations
import io
import json
from pathlib import Path
import pandas as pd
import streamlit as st
from prediction import DEFAULT_MODEL_PATH, load_model, predict_emails

ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "artifacts" / "evaluation.json"
DEMO_PATH = ROOT / "data" / "demo_emails.csv"
st.set_page_config(page_title="MailSense AI", page_icon="📨", layout="wide")

def read_upload(uploaded_file: object) -> pd.DataFrame:
    """Read a CSV or Excel upload."""
    filename = getattr(uploaded_file, "name", "").lower()
    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    raise ValueError("Please upload a CSV or Excel file.")

def main() -> None:
    st.title("📨 MailSense AI")
    st.caption("Intelligent Email Priority & Context Analyzer")
    st.markdown("Turn an email spreadsheet into a clearer review queue. MailSense AI predicts priority and shows estimated confidence alongside terms that influenced the model.")
    with st.sidebar:
        st.header("Your inbox data")
        uploaded = st.file_uploader("Upload email data", type=["csv", "xlsx", "xls"], help="Your file must contain subject and body columns.")
        use_demo = st.checkbox("Use the included demo emails", value=uploaded is None)
        st.divider()
        st.caption("Model: TF-IDF + Logistic Regression")
        st.caption("Labels: Urgent · Normal · Low")

    if not DEFAULT_MODEL_PATH.exists():
        st.warning("The model has not been trained in this environment. Run python train_model.py in the project directory, then restart the app.")
        return
    try:
        model = load_model(DEFAULT_MODEL_PATH)
    except Exception as exc:
        st.error(f"Could not load the trained model: {exc}")
        return

    try:
        if uploaded is not None:
            frame = read_upload(uploaded)
        elif use_demo and DEMO_PATH.exists():
            frame = pd.read_csv(DEMO_PATH)
        else:
            frame = None
    except Exception as exc:
        st.error(f"Could not read the selected file: {exc}")
        return

    if frame is None:
        st.info("Upload a CSV/Excel file or select the demo emails in the sidebar.")
        return
    missing = {"subject", "body"}.difference(frame.columns)
    if missing:
        st.error(f"Missing required column(s): {', '.join(sorted(missing))}")
        return
    if frame.empty:
        st.info("The selected file contains no email rows.")
        return

    st.subheader("Input preview")
    st.dataframe(frame[["subject", "body"]].head(8), use_container_width=True)
    if st.button("Analyze email priorities", type="primary"):
        with st.spinner("Analyzing email text..."):
            try:
                st.session_state["mailsense_results"] = predict_emails(frame, model)
            except Exception as exc:
                st.error(f"Prediction failed: {exc}")
                return

    results = st.session_state.get("mailsense_results")
    if results is None:
        return
    st.subheader("Priority overview")
    counts = results["predicted_priority"].value_counts()
    urgent, normal, low = (int(counts.get(label, 0)) for label in ("Urgent", "Normal", "Low"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Emails analyzed", len(results))
    c2.metric("Urgent", urgent)
    c3.metric("Normal", normal)
    c4.metric("Low", low)
    left, right = st.columns(2)
    with left:
        st.markdown("**Predicted distribution**")
        st.bar_chart(counts)
    with right:
        st.markdown("**Confidence overview**")
        st.metric("Average estimated confidence", f"{results['confidence'].mean():.1f}%")
        st.caption("Confidence is a model probability estimate, not a guarantee of correctness.")
    st.subheader("Classified emails")
    st.dataframe(results, use_container_width=True, hide_index=True)
    output = io.BytesIO()
    results.to_csv(output, index=False)
    st.download_button("Download predictions as CSV", data=output.getvalue(), file_name="mailsense_ai_predictions.csv", mime="text/csv")
    if REPORT_PATH.exists():
        with st.expander("Training evaluation (hold-out sample)"):
            try:
                metrics = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
                st.metric("Hold-out accuracy", f"{metrics['accuracy']:.1%}")
                st.caption(metrics.get("note", ""))
                st.json(metrics["classification_report"])
            except (ValueError, KeyError, OSError):
                st.caption("Evaluation report is unavailable or invalid.")

if __name__ == "__main__":
    main()
