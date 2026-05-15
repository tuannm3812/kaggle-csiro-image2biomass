# CSIRO Image2Biomass EDA

EDA notebook for the Kaggle competition: [CSIRO Biomass](https://www.kaggle.com/competitions/csiro-biomass).

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

## Next Experiments

- Replace simple image features with embeddings from an ImageNet backbone.
- Use grouped cross-validation by image/date/location metadata.
- Train a multi-task image model and blend it with tabular models.
- Add public weather or satellite features by sampling date and state/region.
