# Attribution and project history

## Project owner

MailSense AI is maintained in the GitHub repository owned by [Shiv Verma](https://github.com/shiv2228verma).

## Reference project

The problem domain and feature direction were informed by [Email Priority Classification System by Riya Sinha](https://github.com/riyaacodes/email-priority-classification-system).

The reference repository is publicly marked as **MIT licensed** and its README identifies Riya Sinha as its author. The reference implementation uses SentenceTransformer embeddings from `all-MiniLM-L6-v2` followed by Logistic Regression. Its README reports a 97.3% accuracy figure for that reference project.

## What is different in MailSense AI

MailSense AI is a separately maintained implementation with its own repository structure, Streamlit interface, preprocessing and prediction modules, tests, CI workflow, project documentation, and synthetic demonstration dataset. Its current model is **TF-IDF (unigrams and bigrams) + Logistic Regression**, not the reference project's MiniLM embedding pipeline.

The 97.3% figure shown by the reference repository is **not** a MailSense AI result and must not be attributed to this project. MailSense AI's bundled 40-row synthetic dataset is intended for demonstration and pipeline testing only.

No affiliation, endorsement, or official continuation is claimed. This attribution is provided to acknowledge the reference that informed the project direction. If code or other material from the reference repository is incorporated in a later change, preserve the applicable copyright and MIT license notices and document the reused files.
