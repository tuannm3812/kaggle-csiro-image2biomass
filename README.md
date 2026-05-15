# CSIRO Image2Biomass Kaggle Starter

Starter repo for the Kaggle competition: [CSIRO Biomass](https://www.kaggle.com/competitions/csiro-biomass).

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
|   +-- 01_eda_baseline.ipynb
+-- src/
|   +-- csiro_biomass/
|       +-- __init__.py
|       +-- data.py
|       +-- features.py
|       +-- metrics.py
+-- requirements.txt
+-- kaggle_setup.md
+-- README.md
```

## Kaggle Workflow

This repo is intended to be run inside a Kaggle notebook with the competition input mounted at:

```text
/kaggle/input/competitions/csiro-biomass/
+-- train.csv
+-- test.csv
+-- sample_submission.csv
+-- train/
+-- test/
```

## First Notebook

Open [notebooks/01_eda_baseline.ipynb](notebooks/01_eda_baseline.ipynb). It builds a simple, submission-ready baseline using:

- metadata features from `train.csv`
- simple image color/texture features
- per-target tree models
- competition-style weighted R2 validation
- `/kaggle/working/submission.csv` generation

In Kaggle, upload or paste the notebook, add the competition data, run all cells, and download the output artifacts from the notebook output panel.

The notebook is self-contained. The `src/` package mirrors its helper functions for versioned development, but Kaggle does not need an editable package install.

## Next Experiments

- Replace simple image features with embeddings from an ImageNet backbone.
- Use grouped cross-validation by image/date/location metadata.
- Train a multi-task image model and blend it with tabular models.
- Add public weather or satellite features by sampling date and state/region.
