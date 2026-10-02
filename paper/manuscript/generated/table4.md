: Table 4. Share of the out-of-distribution gap recovered by mitigation, one value per study and mitigation type. *g* uses the in-distribution value as the reference; *g*~o~ uses a target-trained (oracle) model on the same test set. *g* = 0: no recovery; *g* = 1: in-distribution (or oracle) performance restored.

| Mitigation | Studies | Median | IQR | 95% CI of median |
|:--------------------------------------------|--------:|----------:|----------:|------------:|
| *Gap recovered relative to ID, g* | | | | |
| All mitigations | 34 | 0.55 | 0.29–0.83 | 0.40–0.73 |
| Fine-tuning on labelled target data | 9 | 0.89 | 0.84–1.05 | 0.76–1.16 |
| Domain generalisation or augmentation | 11 | 0.60 | 0.28–0.72 | 0.28–0.73 |
| Large-scale or self-supervised pretraining | 4 | 0.35 | 0.28–0.43 | 0.26–0.46 |
| Unsupervised domain adaptation | 10 | 0.28 | 0.06–0.52 | 0.04–0.53 |
| Other | 2 | 0.27 | 0.22–0.32 | 0.18–0.36 |
| *Gap recovered relative to oracle, g~o~* | | | | |
| All mitigations | 16 | 0.71 | 0.61–0.99 | 0.60–0.98 |
| Fine-tuning on labelled target data | 5 | 1.04 | 1.00–1.40 | 0.80–1.97 |
| Domain generalisation or augmentation | 5 | 0.64 | 0.63–0.68 | 0.62–0.73 |
| Unsupervised domain adaptation | 6 | 0.48 | 0.40–0.87 | 0.23–0.98 |
