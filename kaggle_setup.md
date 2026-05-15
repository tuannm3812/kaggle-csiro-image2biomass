# Kaggle Run Notes

## Create a Kaggle Notebook

1. Open the competition page: <https://www.kaggle.com/competitions/csiro-biomass>.
2. Select **Code** then **New Notebook**.
3. Add the competition data as an input dataset.
4. Confirm the input files are available at `/kaggle/input/competitions/csiro-biomass`.
5. Upload or paste the code from `notebooks/01_eda_baseline.ipynb`.
6. Run all cells.

The notebook writes artifacts to:

```text
/kaggle/working/submission.csv
/kaggle/working/train_image_features.csv
/kaggle/working/test_image_features.csv
```

Download `submission.csv` from Kaggle after the notebook finishes.

## Submission Format

The generated CSV must contain exactly:

```text
sample_id,target
ID1001187975__Dry_Green_g,0.0
ID1001187975__Dry_Dead_g,0.0
ID1001187975__Dry_Clover_g,0.0
ID1001187975__GDM_g,0.0
ID1001187975__Dry_Total_g,0.0
```

The starter notebook writes:

```text
/kaggle/working/submission.csv
```
