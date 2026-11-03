# MailSense AI — Model Card

## Model identity

- Project: MailSense AI
- Model type: supervised, three-class text classifier
- Current pipeline: TF-IDF vectorizer + Logistic Regression
- Output labels: Urgent, Normal, Low
- Implementation: scikit-learn Pipeline, trained by train_model.py

## Intended use

This model is intended for learning, software demonstration, and experimentation with prioritizing email-like text records supplied as CSV or Excel files. It is a human-in-the-loop decision-support prototype.

## Out-of-scope use

Do not use this model as the sole basis for deciding whether to ignore, delay, or suppress a real message. It is not validated for safety-critical, legal, medical, financial, security incident, or other high-impact workflows. It does not connect to an email account or perform actions on messages.

## Training data

The bundled file is training_data/sample_training_emails.csv. It contains 40 synthetic, manually authored examples:

| Label | Examples |
|---|---:|
| Urgent | 12 |
| Normal | 13 |
| Low | 15 |
| **Total** | **40** |

The examples are designed to exercise the training pipeline and are not a representative sample of real inbox traffic.

## Preprocessing and features

The project combines each email's subject and body, lowercases text, normalizes whitespace, and converts text into TF-IDF features. The vectorizer uses unigrams and bigrams. The classifier is Logistic Regression with a maximum iteration limit and balanced class weights. The model is trained and evaluated using a stratified hold-out split.

## Outputs

- Predicted priority label.
- Maximum predicted class probability, displayed as estimated confidence.
- Indicative terms based on the fitted classifier coefficients and active TF-IDF features.

The confidence score is not a calibrated guarantee. Indicative terms are model signals, not causal explanations.

## Evaluation

Run python train_model.py to generate the hold-out evaluation report in artifacts/evaluation.json. The report includes accuracy, macro F1, weighted F1, per-class precision/recall/F1, sample counts, and a confusion matrix.

Because the dataset has only 40 synthetic rows, any reported metrics are unstable and should be treated as a pipeline demonstration only. The reference repository's reported metrics are not the metrics of this model. MailSense AI does not claim the reference project's reported 97.3% accuracy.

## Known limitations and risks

- Small synthetic dataset and simplified language.
- Limited coverage of ambiguous, multilingual, domain-specific, and adversarial messages.
- Possible false negatives for urgent messages.
- Training/test performance may not generalize to real-world email distributions.
- Probabilities may be poorly calibrated.
- Training data may contain sensitive information if users upload real messages; avoid shared/public environments for confidential data.

## Recommended next evaluation steps

1. Obtain appropriately consented and de-identified messages.
2. Create a documented annotation guide for the three labels.
3. Have multiple annotators review ambiguous examples and measure agreement.
4. Remove duplicates and near-duplicates across data splits.
5. Keep a representative independent test set.
6. Report per-class precision, recall, F1, confusion matrix, and uncertainty.
7. Compare TF-IDF and transformer embeddings using the same splits and evaluation protocol.