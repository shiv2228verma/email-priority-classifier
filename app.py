"""Streamlit interface for MailSense AI."""
from __future__ import annotations
import hashlib
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

@st.cache_resource
def get_model():
    """Cache the trained pipeline for the lifetime of the Streamlit process."""
    return load_model(DEFAULT_MODEL_PATH)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px;}
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(37,99,235,.10), rgba(14,165,233,.06));
        border: 1px solid rgba(100,116,139,.18);
        padding: 1rem 1.1rem; border-radius: 14px;
    }
    div.stButton > button[kind="primary"] {
        border-radius: 10px; min-height: 2.8rem; font-weight: 650;
    }
    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(100,116,139,.45); border-radius: 12px; padding: .5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def input_fingerprint(frame: pd.DataFrame) -> str:
    """Identify the displayed input so results from an older upload are cleared."""
    hashed_rows = pd.util.hash_pandas_object(frame, index=True).values.tobytes()
    column_names = "|".join(map(str, frame.columns)).encode("utf-8")
    return hashlib.sha256(column_names + hashed_rows).hexdigest()


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
    st.caption("INTELLIGENT EMAIL PRIORITY & CONTEXT ANALYZER")
    st.markdown(
        "Turn an email spreadsheet into a clearer review queue. "
        "Prioritize what needs attention, understand the model's signals, "
        "and export a review-ready result."
    )
    with st.sidebar:
        st.header("Your inbox data")
        uploaded = st.file_uploader("Upload email data", type=["csv", "xlsx", "xls"], help="Your file must contain subject and body columns.")
        use_demo = st.checkbox("Use the included demo emails", value=uploaded is None)
        st.divider()
        st.caption("Model: TF-IDF + Logistic Regression")
        st.caption("Labels: Urgent · Normal · Low")
        st.caption("Privacy: uploaded files are processed by this app session; avoid sensitive data on shared deployments.")

    if not DEFAULT_MODEL_PATH.exists():
        st.warning("The model has not been trained in this environment. Run python train_model.py in the project directory, then restart the app.")
        return
    try:
        model = get_model()
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

    current_fingerprint = input_fingerprint(frame)
    if st.session_state.get("mailsense_input_fingerprint") != current_fingerprint:
        st.session_state.pop("mailsense_results", None)
        st.session_state["mailsense_input_fingerprint"] = current_fingerprint

    st.subheader("Input preview")
    st.caption(f"{len(frame):,} email row(s) loaded · showing the first 8")
    st.dataframe(frame[["subject", "body"]].head(8), use_container_width=True)
    with st.expander("How MailSense AI handles your data"):
        st.write(
            "The uploaded spreadsheet is read for this analysis and is not "
            "connected to a mailbox. This prototype does not send, delete, "
            "or move emails. Avoid uploading confidential or personal email "
            "content to a public or shared deployment."
        )
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
                m1, m2, m3 = st.columns(3)
                m1.metric("Hold-out accuracy", f"{metrics['accuracy']:.1%}")
                m2.metric("Macro F1", f"{metrics['macro_f1']:.3f}")
                m3.metric("Weighted F1", f"{metrics['weighted_f1']:.3f}")
                st.caption(
                    f"Training rows: {metrics['train_samples']} · "
                    f"Test rows: {metrics['test_samples']} · "
                    + metrics.get("note", "")
                )
                st.markdown("**Confusion matrix** (rows = actual, columns = predicted)")
                matrix = pd.DataFrame(
                    metrics["confusion_matrix"],
                    index=metrics["class_order"],
                    columns=metrics["class_order"],
                )
                st.dataframe(matrix, use_container_width=True)
                st.markdown("**Per-class classification report**")
                st.json(metrics["classification_report"])
            except (ValueError, KeyError, OSError):
                st.caption("Evaluation report is unavailable or invalid.")

if __name__ == "__main__":
    main()
