# CSIRO Image2Biomass

<p>
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-CSIRO%20Biomass-20BEFF?style=flat&logo=kaggle&logoColor=white" height="20">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white" height="20">
  <img alt="Notebook" src="https://img.shields.io/badge/Notebook-EDA%20%2B%20Baseline-F37626?style=flat&logo=jupyter&logoColor=white" height="20">
  <img alt="Status" src="https://img.shields.io/badge/Status-Active%20Research-2E7D32?style=flat" height="20">
</p>

<p>
  <img src="https://reneweconomy.com.au/wp-content/uploads/2021/02/redbank-power-station-hunter-energy-optimised.jpg" alt="Agricultural biomass landscape" width="520">
</p>

Kaggle workflow for the [CSIRO Image2Biomass Prediction](https://www.kaggle.com/competitions/csiro-biomass) competition. The project explores pasture image, metadata, and measurement signals before building baseline models for biomass prediction.

The task is to predict five pasture biomass targets for each image:

- `Dry_Green_g`
- `Dry_Dead_g`
- `Dry_Clover_g`
- `GDM_g`
- `Dry_Total_g`

The competition uses one global weighted R2 over all image-target rows. Target weights are:

| target | weight |
| --- | ---: |
| `Dry_Green_g` | 0.1 |
| `Dry_Dead_g` | 0.1 |
| `Dry_Clover_g` | 0.1 |
| `GDM_g` | 0.2 |
| `Dry_Total_g` | 0.5 |

## Repo Layout

```text
.
+-- notebooks/
|   +-- 01_deep_dive_eda.ipynb
|   +-- 02_baseline_models.ipynb
+-- README.md
```

## Kaggle Workflow

This repo is intended to run inside Kaggle notebooks with the competition input mounted at:

```text
/kaggle/input/competitions/csiro-biomass/
+-- train.csv
+-- test.csv
+-- sample_submission.csv
+-- train/
+-- test/
```

## First Notebook

Open [notebooks/01_deep_dive_eda.ipynb](notebooks/01_deep_dive_eda.ipynb). It focuses on deep exploratory analysis:

- data quality checks
- metric weight analysis
- target distributions and image-level target accounting
- state, species, date, NDVI, and height effects
- train-test metadata drift
- simple image color/texture signals
- visual image audit grids
- outlier review exports
- lightweight baseline error diagnostics for insight generation

In Kaggle, upload or paste the notebook, add the competition data, run all cells, and download the output artifacts from the notebook output panel.

The notebook is self-contained and assumes Kaggle's standard Python environment. It writes EDA artifacts to `/kaggle/working`:

```text
eda_insights.csv
eda_outlier_review.csv
eda_segment_error.csv
train_image_features.csv
test_image_features.csv
```

## EDA Findings

Current EDA output points to a few modeling priorities:

- `Dry_Total_g` is the most important target for the leaderboard because it carries 50% of the effective metric weight.
- `Dry_Total_g` also has the widest spread and the highest lightweight-model MAE, so calibration here should be treated as the first modeling priority.
- `Dry_Total_g` exactly matches the component sum in the EDA checks, making target relationship constraints useful as validation sanity checks and possible post-processing.
- `Height_Ave_cm` has strong monotonic signal for `Dry_Green_g` with Spearman correlation around `0.80`.
- `Pre_GSHH_NDVI` is most associated with `GDM_g`, with Spearman correlation around `0.59`.
- Simple image greenness features are useful: `excess_green` is strongest against `GDM_g`, around `0.52`.

Hardest diagnostic segments from the lightweight EDA model:

| target | state | MAE | bias | target mean |
| --- | --- | ---: | ---: | ---: |
| `Dry_Total_g` | NSW | 18.86 | -0.57 | 70.90 |
| `Dry_Green_g` | NSW | 14.78 | -0.03 | 56.56 |
| `GDM_g` | NSW | 14.75 | 1.36 | 56.69 |
| `Dry_Clover_g` | WA | 11.17 | -1.21 | 22.09 |
| `Dry_Total_g` | Tas | 9.88 | -0.22 | 36.80 |

Outlier review suggests many legitimate zero-valued clover and dead-matter rows, especially where species composition does not include clover or where WA samples have no dead matter. High-biomass NSW rows should be visually reviewed because they dominate the largest `Dry_Total_g`, `Dry_Green_g`, and `GDM_g` extremes.

## Baseline Models

Open [notebooks/02_baseline_models.ipynb](notebooks/02_baseline_models.ipynb) after running the EDA notebook. It:

- reviews available EDA output artifacts
- uses grouped cross-validation by `image_path`
- drops train-only metadata when the Kaggle test file does not provide it
- trains with metric-aligned target weights
- compares median, ridge, histogram gradient boosting, and extra-trees baselines
- reports global weighted R2 plus per-target and segment diagnostics
- validates whether enforcing `Dry_Total_g = Dry_Green_g + Dry_Dead_g + Dry_Clover_g` improves local score
- writes `/kaggle/working/submission.csv`

It also exports:

```text
baseline_cv_summary.csv
baseline_per_target.csv
baseline_segment_error.csv
submission.csv
```

## Next Experiments

- Replace simple image features with embeddings from an ImageNet backbone.
- Use grouped cross-validation by image/date/location metadata.
- Train a multi-task image model and blend it with tabular models.
- Add public weather or satellite features by sampling date and state/region.
