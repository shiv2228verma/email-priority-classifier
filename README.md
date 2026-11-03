# MailSense AI

**Intelligent Email Priority & Context Analyzer**

![Python tests](https://github.com/shiv2228verma/email-priority-classifier/actions/workflows/tests.yml/badge.svg?branch=feature%2Fmailsense-ai-foundation)

MailSense AI is a student-built machine-learning prototype that analyzes email subject/body text and predicts one of three priority levels: **Urgent**, **Normal**, or **Low**. It provides a Streamlit dashboard for CSV/Excel uploads, prediction review, evaluation summaries, and CSV export.

> This project was developed in the repository owned by [Shiv Verma](https://github.com/shiv2228verma). Its problem domain and feature inspiration were informed by the reference project listed in [ATTRIBUTION.md](ATTRIBUTION.md). MailSense AI is not the original author's repository or an official continuation.

## Problem statement

Busy inboxes contain urgent incidents, routine work updates, and optional messages. Manually sorting exported email data can take time and may cause important messages to be missed. MailSense AI explores how a supervised text classifier can assist a person by suggesting a priority label for each email record.

The tool is a decision-support prototype. It does not connect to a live mailbox or take actions on emails.

## Features

- Load the included demonstration email dataset or upload a CSV/Excel file.
- Validate required subject and body columns.
- Normalize text consistently for training and prediction.
- Predict Urgent, Normal, or Low priority.
- Display estimated class confidence and indicative model terms.
- View priority counts and a distribution chart.
- Review hold-out evaluation metrics and a confusion matrix.
- Export the classified rows to CSV.
- Automatically train the included demo model on first launch if no saved model exists.
- Run automated tests and model-training checks through GitHub Actions.

## Model and technology

The current baseline is **TF-IDF (unigrams and bigrams) + Logistic Regression**. It is implemented as a scikit-learn Pipeline.

| Technology | Use |
|---|---|
| Python | Application and model code |
| Streamlit | Interactive dashboard |
| Pandas | CSV/Excel data handling |
| Scikit-learn | TF-IDF, Logistic Regression, and evaluation |
| Joblib | Model persistence |
| OpenPyXL / xlrd | Excel file support |
| Pytest | Automated tests |
| GitHub Actions | Continuous integration |

The reference repository uses SentenceTransformer embeddings from `all-MiniLM-L6-v2` with Logistic Regression. The current MailSense AI implementation uses TF-IDF instead; transformer embeddings are a possible future comparison, not an existing feature.

## Architecture

```text
CSV / Excel email records
          |
          v
Validate subject and body
          |
          v
Text normalization
          |
          v
TF-IDF vectorization
          |
          v
Logistic Regression
          |
          +----> Predicted priority
          +----> Estimated probability
          +----> Indicative terms
          |
          v
Streamlit dashboard
          |
          v
CSV export
```

## Project structure

```text
email-priority-classifier/
├── app.py
├── preprocessing.py
├── prediction.py
├── train_model.py
├── requirements.txt
├── START_MAILSENSE_WINDOWS.bat
├── data/
│   └── demo_emails.csv
├── training_data/
│   └── sample_training_emails.csv
├── artifacts/                    # generated model/report; not committed
├── tests/
│   ├── test_preprocessing.py
│   └── test_prediction.py
├── docs/
│   ├── DATASET_CARD.md
│   ├── MODEL_CARD.md
│   ├── PROJECT_GUIDE.md
│   └── PROJECT_STATEMENT.md
├── .github/workflows/tests.yml
├── .streamlit/config.toml
├── pytest.ini
├── .gitignore
├── ATTRIBUTION.md
├── LICENSE
└── README.md
```

## Installation and setup

**Requirements:** Python 3.10 or newer.

### Windows — easiest method

1. Download or clone this repository.
2. Open the project folder.
3. Double-click `START_MAILSENSE_WINDOWS.bat`.
4. Wait while it creates the virtual environment, installs dependencies, and starts Streamlit.
5. Open the local address shown in the terminal (normally http://localhost:8501).

Keep the terminal window open while using the dashboard. The first setup requires an internet connection to install Python packages.

### Manual setup

Clone the feature branch:

```bash
git clone --branch feature/mailsense-ai-foundation https://github.com/shiv2228verma/email-priority-classifier.git
cd email-priority-classifier
```

Create and activate a virtual environment.

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and start the dashboard:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

On first launch, the app automatically trains the small bundled demo model and saves it in `artifacts/`. To retrain it manually:

```bash
python train_model.py
```

## Input data format

Upload a CSV or Excel workbook containing these two required columns:

| Column | Meaning |
|---|---|
| `subject` | Email subject; blank values are allowed |
| `body` | Email body; blank values are allowed |

Example:

```csv
subject,body
"Server outage","The production API is unavailable."
"Weekly update","Here is the routine team progress summary."
```

Column names are case-sensitive in this version. The prediction input does not need a priority/label column.

## Training dataset and evaluation

The bundled training file is `training_data/sample_training_emails.csv`. It contains **40 synthetic, manually authored examples**:

| Priority | Rows |
|---|---:|
| Urgent | 12 |
| Normal | 13 |
| Low | 15 |
| **Total** | **40** |

The training script uses a stratified train/test split (fixed random seed), then reports accuracy, macro F1, weighted F1, per-class precision/recall/F1, and a confusion matrix. The generated model and report are saved under `artifacts/`.

**Important evaluation limitation:** the dataset is very small and synthetic. Its score is only a demonstration of the pipeline and is not evidence of production performance. Do not report the reference repository's 97.3% result as a MailSense AI result. A reliable evaluation requires a larger, representative, independently labelled dataset.

The confidence column is the classifier's estimated class probability, not a guarantee of correctness. Indicative terms are coefficient-based model signals, not causal explanations.

## Run tests

```bash
pytest -q
```

The GitHub Actions workflow also checks Python syntax, runs the tests, and executes a model-training smoke test.

## Documentation

- [Project statement](docs/PROJECT_STATEMENT.md) — problem, objectives, scope, users, workflow, technology, and limitations.
- [Project guide](docs/PROJECT_GUIDE.md) — architecture, algorithm, metrics, demo instructions, and viva questions.
- [Model card](docs/MODEL_CARD.md) — intended use, training data, evaluation, and model risks.
- [Dataset card](docs/DATASET_CARD.md) — sample dataset details and limitations.
- [Attribution and project history](ATTRIBUTION.md) — reference project and license acknowledgement.

## Limitations and responsible use

- This is a prototype, not a production email client.
- It does not integrate with Gmail or Outlook and cannot send, delete, archive, or move messages.
- Performance may be poor on messages unlike the small synthetic training examples.
- False negatives are possible, including for urgent messages.
- Do not upload confidential or regulated email content to public/shared deployments.
- A person must review important messages; do not use the model as the sole reason to ignore or delay communication.

## Roadmap

- [ ] Build a larger, consented, independently labelled dataset.
- [ ] Add cross-validation, error analysis, and probability calibration.
- [ ] Compare TF-IDF with SentenceTransformer embeddings using the same evaluation split.
- [ ] Improve confusion-matrix visualization and configurable threshold experiments.
- [ ] Capture genuine application screenshots after local UI verification.
- [ ] Add deployment instructions and deploy only after testing privacy and resource requirements.
- [ ] Explore mailbox integration only with explicit user consent and appropriate security controls.

## Author

**Shiv Verma** — [GitHub: @shiv2228verma](https://github.com/shiv2228verma)

See [ATTRIBUTION.md](ATTRIBUTION.md) for the project's reference and history.
