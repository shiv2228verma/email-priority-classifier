# MailSense AI

**Intelligent Email Priority & Context Analyzer**

![Python tests](https://github.com/shiv2228verma/email-priority-classifier/actions/workflows/tests.yml/badge.svg?branch=feature%2Fmailsense-ai-foundation)

MailSense AI is an independent, student-built machine-learning prototype that classifies email messages as **Urgent**, **Normal**, or **Low** priority. It uses consistent text preprocessing, TF-IDF features, and Logistic Regression in an interactive Streamlit dashboard.

> This is an independent implementation inspired by the email-prioritization idea referenced in [ATTRIBUTION.md](ATTRIBUTION.md). It is not the original author's repository or an official continuation.

## Features
- Upload email datasets in CSV or Excel format.
- Validate and normalize subject and body text.
- Predict Urgent, Normal, or Low priority.
- Show estimated class confidence and influential text terms.
- Explore priority counts and average confidence.
- Download predictions as a CSV report.
- Evaluate the model on a stratified hold-out split.
- Run automated tests with pytest and GitHub Actions.

## Architecture
    Subject + body
         |
         v
    Text normalization
         |
         v
    TF-IDF vectorizer
         |
         v
    Logistic Regression
         |
         +--> Priority label
         +--> Estimated probability
         +--> Influential terms
         |
         v
    Streamlit dashboard and CSV export

The initial baseline intentionally uses TF-IDF + Logistic Regression. It is lightweight and reproducible. Transformer embeddings can be evaluated as a future model comparison rather than claimed as an existing feature.

## Project structure
    email-priority-classifier/
    ├── app.py
    ├── preprocessing.py
    ├── prediction.py
    ├── train_model.py
    ├── requirements.txt
    ├── data/demo_emails.csv
    ├── training_data/sample_training_emails.csv
    ├── artifacts/                 # generated locally; not committed
    ├── tests/
    ├── .github/workflows/tests.yml
    ├── .streamlit/config.toml
    ├── docs/
    ├── tests/
    ├── .gitignore
    ├── ATTRIBUTION.md
    └── README.md

## Setup

1. Clone the repository:
       git clone https://github.com/shiv2228verma/email-priority-classifier.git
       cd email-priority-classifier

2. Create and activate a virtual environment.

   Windows PowerShell:
       py -m venv .venv
       .venv\Scripts\Activate.ps1

   macOS or Linux:
       python3 -m venv .venv
       source .venv/bin/activate

3. Install dependencies and train the model:
       python -m pip install --upgrade pip
       pip install -r requirements.txt
       python train_model.py

4. Launch the dashboard:
       streamlit run app.py

Open the local URL printed by Streamlit (normally http://localhost:8501).

## Input format

Upload a CSV or Excel workbook containing these required columns:

| Column | Description |
|---|---|
| subject | Email subject; blank values are allowed |
| body | Email body; blank values are allowed |

Example:
    subject,body
    "Server outage","The production API is unavailable."
    "Weekly update","Here is the routine team progress summary."

Column names are case-sensitive in this first version.

## Model evaluation

Running \`python train_model.py\` creates \`artifacts/priority_model.joblib\` and \`artifacts/evaluation.json\`. It prints accuracy and a per-class precision, recall, and F1 report based on a stratified hold-out split.

**Evaluation caution:** The included labelled dataset is small and illustrative. Its score is not evidence of production performance. Replace it with a larger, representative, carefully labelled dataset and evaluate on a separate test set before making real-world claims.

The confidence field is the classifier's estimated class probability, not a guarantee of correctness. Influential terms are model-based indicators, not proof of causation.

## Tests
    pytest -q

## Developer documentation

- [Technical project walkthrough](docs/PROJECT_GUIDE.md) — architecture, algorithm, metrics, demonstration steps, and viva preparation.
- [Dataset card](docs/DATASET_CARD.md) — sample data origin, class distribution, intended use, and limitations.
- [Attribution and project history](ATTRIBUTION.md) — acknowledgement of the project idea that inspired this work.

## Limitations and responsible use
- This is a decision-support prototype, not an autonomous email client.
- It does not connect to Gmail or Outlook and cannot send, delete, or move messages.
- Predictions may reflect gaps or bias in the training data.
- Do not upload confidential or regulated email content to an environment you do not control.
- Review important messages yourself; do not rely on this prototype as the sole reason to ignore or delay communication.

## Roadmap
- [ ] Evaluate on a larger, independently labelled dataset.
- [ ] Compare the TF-IDF baseline with sentence-transformer embeddings.
- [ ] Add confusion-matrix visualizations and configurable thresholds.
- [ ] Add verified screenshots and deployment instructions.
- [ ] Explore optional mailbox integrations with explicit user consent.

## Author
**Shiv Verma** — [@shiv2228verma](https://github.com/shiv2228verma)

See [ATTRIBUTION.md](ATTRIBUTION.md) for project inspiration and history.
