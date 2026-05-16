# CSIRO Image2Biomass

<p>
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-CSIRO%20Biomass-20BEFF?style=flat&logo=kaggle&logoColor=white" height="20">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white" height="20">
  <img alt="Notebook" src="https://img.shields.io/badge/Notebook-EDA%20%2B%20Baseline%20%2B%20Experiments-F37626?style=flat&logo=jupyter&logoColor=white" height="20">
  <img alt="Status" src="https://img.shields.io/badge/Status-Active%20Research-2E7D32?style=flat" height="20">
</p>

![Bioenergy pasture banner](https://arena.gov.au/assets/2019/06/bioenergy-banner.jpg)

Kaggle workflow for the [CSIRO Image2Biomass Prediction](https://www.kaggle.com/competitions/csiro-biomass) competition. The project concludes with a validated tabular/color modeling workflow and a product direction for an AI-assisted pasture biomass decision support tool.

## 1. Objective

Predict five biomass targets for each pasture image:

| target | metric weight | role |
| --- | ---: | --- |
| `Dry_Green_g` | 0.1 | green biomass component |
| `Dry_Dead_g` | 0.1 | dead biomass component |
| `Dry_Clover_g` | 0.1 | clover biomass component |
| `GDM_g` | 0.2 | green dry matter |
| `Dry_Total_g` | 0.5 | highest-impact total biomass target |

The competition metric is one global weighted R2 over all image-target rows. `Dry_Total_g` receives 50% of the effective metric weight, so total-biomass accuracy and the accounting constraint are central to model selection.

## 2. Repository

```text
.
+-- notebooks/
|   +-- 01_deep_dive_eda.ipynb
|   +-- 02_baseline_models.ipynb
|   +-- 03_image_embedding_experiments.ipynb
|   +-- 04_tabular_model_tuning.ipynb
+-- README.md
```

Run notebooks on Kaggle with competition data mounted at:

```text
/kaggle/input/competitions/csiro-biomass/
```

## 3. Notebook Workflow

1. `notebooks/01_deep_dive_eda.ipynb`
   - Validates data shape, missing values, target consistency, metric weights, metadata signal, image color signal, outliers, and early segment errors.
   - Exports EDA artifacts such as `eda_insights.csv`, `eda_segment_error.csv`, and image color feature CSVs.

2. `notebooks/02_baseline_models.ipynb`
   - Establishes the stable benchmark using `GroupKFold(image_path)`, metric-aligned sample weights, tabular metadata, and simple image color features.
   - Compares median, ridge, HGB, and ExtraTrees baselines.
   - Validates the biomass accounting constraint before applying it.
   - Exports `submission.csv` and baseline diagnostic CSVs.

3. `notebooks/03_image_embedding_experiments.ipynb`
   - Tests TorchVision EfficientNet-B0 embeddings, PCA-reduced embeddings, Ridge/log-Ridge variants, and ExtraTrees.
   - Bundles experiment artifacts into `embedding_experiment_artifacts.zip`.
   - Current conclusion: EfficientNet-B0 embeddings underperform the tabular/color baseline and should not be promoted yet.

4. `notebooks/04_tabular_model_tuning.ipynb`
   - Tunes the strongest tabular/color feature set with focused ExtraTrees and HGB sweeps.
   - Tests OOF blends between the best ExtraTrees and HGB models.
   - Re-validates the biomass total constraint.
   - Exports `tabular_tuning_artifacts.zip`, including `tabular_tuning_promotion_review.csv`.

## 4. Final Research Results

### Stable Baseline

| model | weighted R2 | constrained R2 | MAE | note |
| --- | ---: | ---: | ---: | --- |
| `extra_trees` | 0.8081 | 0.8114 | 6.82 | current stable reference |
| `hgb` | 0.7958 | not promoted | 7.47 | useful blend candidate |
| `ridge_log` | 0.6449 | not promoted | 10.60 | too weak |
| `dummy_median` | -0.0376 | not promoted | 20.45 | sanity baseline |

The biomass constraint `Dry_Total_g = Dry_Green_g + Dry_Dead_g + Dry_Clover_g` consistently helps the best tabular/color models and is applied only when validated by OOF CV.

### Embedding Experiments

| experiment family | best model | constrained R2 | conclusion |
| --- | --- | ---: | --- |
| tabular/color reference | ExtraTrees | 0.8110 | still strongest in notebook 03 |
| EfficientNet-B0 embeddings | ExtraTrees | 0.6447 | not competitive |
| image color + embeddings | ExtraTrees | 0.6417 | not competitive |
| PCA embeddings | ExtraTrees | 0.6065 | not competitive |
| Ridge/log-Ridge embeddings | Ridge variants | <= 0.4803 | not competitive |

EfficientNet-B0 features are useful as a diagnostic experiment, but they are not part of the promoted modeling path.

### Tabular Tuning

| candidate | raw weighted R2 | constrained R2 | note |
| --- | ---: | ---: | --- |
| `blend_et0.70_hgb0.30` | 0.8128 | 0.8182 | best global CV so far |
| `blend_et0.75_hgb0.25` | 0.8124 | 0.8181 | similar score, slightly lower MAE |
| `blend_et0.65_hgb0.35` | 0.8131 | 0.8180 | similar score |
| `et_leaf3_mf050` | 0.8067 | 0.8126 | best individual tuned model |

The tuned blend improves global CV by about `+0.0066` over the stable constrained baseline. Promotion is guarded by hard-segment checks because the highest-scoring blend can worsen some NSW and WA segment MAE.

Final modeling conclusion: the best research candidate is `70%` tuned ExtraTrees, `30%` HGB, followed by the validated biomass accounting constraint. The stable production candidate should still include segment-risk flags.

## 5. Key Insights

- `Dry_Total_g` dominates the metric and should remain the first target to monitor.
- The total biomass accounting relationship is strong and should be treated as validated post-processing, not assumed blindly.
- Metadata and simple color features outperform first-pass CNN embeddings on this small training set.
- ExtraTrees remains the strongest individual model family; HGB is weaker alone but useful in blends.
- The main risk is improving global weighted R2 while worsening high-impact segments.

Hard segments to monitor in every experiment:

| target | state | reason |
| --- | --- | --- |
| `Dry_Total_g` | NSW | highest weighted target, high biomass |
| `GDM_g` | NSW | high biomass and 0.2 metric weight |
| `Dry_Green_g` | NSW | high-biomass green component |
| `Dry_Clover_g` | WA | persistent clover error segment |

## 6. Product Concept

### Pasture Biomass Decision Support Tool

The research can be translated into a practical AI product for pasture monitoring. The product would estimate biomass from a pasture image and optional metadata, then use an AI agent to turn model outputs into context-aware recommendations.

Core prediction outputs:

- `Dry_Green_g`
- `Dry_Dead_g`
- `Dry_Clover_g`
- `GDM_g`
- `Dry_Total_g`
- constraint-corrected total biomass
- hard-segment risk flags

AI-agent layer:

- Explains prediction drivers in plain language.
- Flags uncertain or high-risk cases, especially NSW high-biomass and WA clover-like cases.
- Suggests next actions such as inspect paddock, collect height/NDVI metadata, defer grazing, increase monitoring frequency, or review pasture composition.
- Produces farmer-facing summaries and agronomist-facing diagnostics.

Example recommendation flow:

1. User uploads a pasture image and enters optional paddock metadata.
2. Biomass model estimates target values and applies validated post-processing.
3. Risk checker compares the case against known weak segments.
4. AI agent generates a recommendation with caveats and suggested follow-up measurements.

Recommended positioning:

- Use as an **AI-assisted pasture biomass estimation and monitoring tool**.
- Do not position it as fully automated agronomy or crop prescription.
- Keep recommendations advisory and grounded in model confidence, local context, and user-provided metadata.

## 7. Promotion Rules

Promote a model only when it satisfies all of the following:

1. Uses `GroupKFold(image_path)` validation.
2. Beats the stable constrained baseline near `0.8116` weighted R2.
3. Applies the biomass constraint only if OOF validation improves.
4. Does not materially worsen the monitored hard segments.
5. Produces downloadable artifacts for review.

For notebook 04, review `tabular_tuning_promotion_review.csv` before replacing the stable baseline.

## 8. Project Closeout

1. Research phase complete: EDA, baseline, embeddings, and tabular tuning have been explored.
2. Archive EfficientNet-B0 as a negative result for this dataset and modeling setup.
3. Treat the tuned blend as the best global CV candidate, with hard-segment warnings.
4. Use notebook 04 artifacts to decide whether to promote the blend or keep the stable baseline.
5. Productize the work as a decision support tool with an AI-agent recommendation layer.
