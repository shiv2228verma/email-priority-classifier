# MailSense AI — Project Statement

## 1. Problem statement

People and teams receive emails with very different levels of importance. A message about a service outage, a security incident, or a blocked payment may need immediate attention, while a routine meeting update or optional newsletter can usually wait. When inboxes are busy, manually sorting messages takes time and important communication can be overlooked.

MailSense AI explores a machine-learning approach to help users review email datasets by predicted priority. It analyzes the subject and body of each email and assigns one of three labels: **Urgent**, **Normal**, or **Low**. The application is intended to support human review, not replace human judgment.

## 2. Project objectives

- Build a reproducible text-classification pipeline for email priority prediction.
- Apply consistent text preprocessing to email subjects and bodies.
- Convert text into numerical features using TF-IDF.
- Train a Logistic Regression classifier for three priority classes.
- Present predictions and estimated class probabilities in a Streamlit dashboard.
- Show model-indicative terms to help users inspect predictions.
- Summarize predicted priority counts and provide downloadable CSV results.
- Evaluate the baseline using a stratified hold-out split and standard classification metrics.

## 3. Scope of the project

### Included in the current version

- Upload email data as CSV or Excel (.xlsx and .xls).
- Read the required subject and body columns.
- Handle blank subject/body cells and normalize text.
- Predict Urgent, Normal, or Low priority.
- Display estimated confidence and indicative terms.
- Show a priority distribution chart and evaluation information.
- Export classified results as a CSV file.
- Train the included demonstration model automatically on first app launch.
- Run automated tests and a model-training smoke test through GitHub Actions.

### Not included in the current version

- Direct connection to Gmail, Outlook, IMAP, or SMTP.
- Reading a user's live inbox or accessing email credentials.
- Sending, deleting, archiving, moving, or replying to emails.
- Push notifications, automated escalation, or background inbox monitoring.
- User accounts, a production database, or enterprise deployment controls.
- A transformer/Sentence-BERT embedding model. The current baseline uses TF-IDF.

These may be explored in later versions with appropriate security, consent, and testing.

## 4. Intended users

- Students learning Natural Language Processing and supervised machine learning.
- Developers exploring text classification and Streamlit applications.
- Small teams that want to experiment with prioritizing exported email datasets.
- IT/helpdesk or operations teams evaluating a prototype on approved, non-sensitive sample data.

The current small synthetic dataset is for demonstration and software testing; it is not validated for operational decisions.

## 5. High-level system workflow

1. The user selects the included demonstration emails or uploads a CSV/Excel file.
2. The application checks that the subject and body columns exist.
3. Text is normalized using the shared preprocessing functions.
4. The trained TF-IDF vectorizer converts text into numerical features.
5. Logistic Regression predicts a priority class and class probabilities.
6. The dashboard displays the predicted label, estimated confidence, and indicative terms.
7. The user reviews the output and may download it as a CSV file.

## 6. Technology stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Tabular data loading and processing |
| Scikit-learn | TF-IDF, Logistic Regression, train/test split, and evaluation |
| Streamlit | Interactive web dashboard |
| Joblib | Saving and loading the trained model |
| OpenPyXL / xlrd | Excel workbook support |
| Pytest | Automated unit tests |
| GitHub Actions | Continuous integration checks |

## 7. Model and evaluation

The current baseline is a scikit-learn Pipeline containing a TF-IDF vectorizer with unigram and bigram features and a Logistic Regression classifier. The training script uses a stratified train/test split with a fixed random seed and reports accuracy, macro F1, weighted F1, a per-class classification report, and a confusion matrix.

The included training data contains 40 synthetic examples: 12 Urgent, 13 Normal, and 15 Low. This is deliberately small. Any score produced from it is a demonstration of the training/evaluation workflow, not a reliable estimate of performance on real inboxes. No claim of 97.3% accuracy is made for MailSense AI.

## 8. Limitations and responsible use

- Predictions depend on the quality and representativeness of labelled training data.
- The included synthetic dataset is too small for production use or general performance claims.
- Model confidence is an estimated probability, not certainty; probabilities may not be calibrated.
- Indicative terms describe model features, not causal explanations.
- Important or time-sensitive messages must be reviewed by a person.
- Do not upload confidential, personal, or regulated email content to public or shared deployments.

## 9. Future enhancements

- Build and evaluate a larger, consented, independently labelled dataset.
- Compare TF-IDF with SentenceTransformer embeddings on the same held-out evaluation data.
- Add cross-validation, probability calibration, and error analysis.
- Improve confusion-matrix visualization and allow threshold experiments.
- Add verified application screenshots and deployment documentation.
- Consider optional mailbox integration only after security and explicit-consent requirements are designed and tested.