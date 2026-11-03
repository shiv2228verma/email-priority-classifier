# Dataset card — MailSense AI sample data

## Dataset identity

- File: `training_data/sample_training_emails.csv`
- Type: small, hand-authored demonstration dataset
- Rows: 40 labelled examples
- Fields: `subject`, `body`, `priority`
- Labels: `Urgent`, `Normal`, `Low`

## Label distribution

| Label | Rows |
|---|---:|
| Urgent | 12 |
| Normal | 13 |
| Low | 15 |
| **Total** | **40** |

## Intended use

The dataset exists to make the training pipeline reproducible and to demonstrate the dashboard end to end. It is suitable for software smoke tests and classroom demonstrations.

## Not suitable for

- Claims about production email classification quality.
- Benchmarking against published datasets.
- Making decisions about real people's communications.
- Generalizing across industries, languages, cultures, or organizations.

## Collection and privacy

The examples are synthetic and manually authored for this repository. They are not a sample of private inboxes and contain no real email addresses or message threads.

## Known limitations

- Very small sample size.
- Simplified wording and deliberately obvious label cues.
- No broad representation of ambiguous or borderline emails.
- No multi-language coverage.
- No formal independent label review.
- A random hold-out score on this small set has high uncertainty.

## Recommendation

For a serious evaluation, collect appropriately consented and de-identified messages, define a written annotation guide, use multiple annotators for ambiguous examples, measure agreement, remove near-duplicates across splits, and reserve a separate test set that is not used during model development.
