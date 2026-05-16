# CSIRO Image2Biomass

<p>
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-CSIRO%20Biomass-20BEFF?style=flat&logo=kaggle&logoColor=white" height="20">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white" height="20">
  <img alt="Notebook" src="https://img.shields.io/badge/Notebook-EDA%20%2B%20Baseline%20%2B%20Experiments-F37626?style=flat&logo=jupyter&logoColor=white" height="20">
  <img alt="Status" src="https://img.shields.io/badge/Status-Active%20Research-2E7D32?style=flat" height="20">
</p>

![Bioenergy pasture banner](https://arena.gov.au/assets/2019/06/bioenergy-banner.jpg)

Kaggle workflow for the [CSIRO Image2Biomass Prediction](https://www.kaggle.com/competitions/csiro-biomass) competition. The current focus is a reliable validation setup, concise EDA, and a strong first tabular baseline.

## 1. Objective

Predict five pasture biomass targets for each image:

- `Dry_Green_g`
- `Dry_Dead_g`
- `Dry_Clover_g`
- `GDM_g`
- `Dry_Total_g`

The leaderboard metric is one global weighted R2 over all image-target rows. `Dry_Total_g` is the highest-priority target because it carries 50% of the effective metric weight.

| target | weight |
| --- | ---: |
| `Dry_Green_g` | 0.1 |
| `Dry_Dead_g` | 0.1 |
| `Dry_Clover_g` | 0.1 |
| `GDM_g` | 0.2 |
| `Dry_Total_g` | 0.5 |

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

Run the notebooks on Kaggle with competition data mounted at:

```text
/kaggle/input/competitions/csiro-biomass/
```

## 3. Notebook Workflow

1. `notebooks/01_deep_dive_eda.ipynb`
   - Checks data quality, target structure, metric weights, metadata signals, image color features, outliers, and lightweight baseline error patterns.
   - Exports `eda_insights.csv`, `eda_outlier_review.csv`, `eda_segment_error.csv`, `train_image_features.csv`, and `test_image_features.csv`.

2. `notebooks/02_baseline_models.ipynb`
   - Uses `GroupKFold` by `image_path`, metric-aligned sample weights, simple image features, and available metadata.
   - Compares median, ridge, histogram gradient boosting, and extra-trees baselines.
   - Adds cached EfficientNet-B0 image embeddings when pretrained `torchvision` weights are available.
   - Selects the final submission-safe feature family by grouped CV.
   - Tests target-specific models for `Dry_Total_g`, `GDM_g`, and `Dry_Green_g`.
   - Exports baseline summaries and `submission.csv`.

3. `notebooks/03_image_embedding_experiments.ipynb`
   - Keeps image-embedding experiments separate from the stable baseline notebook.
   - Compares image color features, optional EfficientNet-B0 embeddings, and PCA-reduced embeddings.
   - Skips pretrained embeddings cleanly when internet is disabled and no local weights are available.
   - Reports grouped CV, per-target metrics, and target/state segment errors for promotion decisions.

4. `notebooks/04_tabular_model_tuning.ipynb`
   - Focuses on the current strongest tabular/color feature set after EfficientNet-B0 underperformed.
   - Runs a focused ExtraTrees and HGB tuning sweep.
   - Tests OOF blends between the best ExtraTrees and HGB models.
   - Re-validates the biomass total constraint and exports tuning artifacts.

## 4. Current EDA Insights

- Dataset shape: 357 train images, 1 public test image, and 5 target rows per image.
- Data quality: no missing columns in the latest EDA run; train/test sample IDs are unique.
- Target accounting: `Dry_Total_g` is effectively the sum of `Dry_Green_g`, `Dry_Dead_g`, and `Dry_Clover_g`.
- Strong metadata signals:
  - `Height_Ave_cm` vs `Dry_Green_g`: Spearman around `0.80`.
  - `Pre_GSHH_NDVI` vs `GDM_g`: Spearman around `0.59`.
- Useful simple image signals:
  - `excess_green`, `visible_ndvi_proxy`, and `green_red_ratio` are most useful for green biomass and `GDM_g`.
- Hardest lightweight-baseline segments:

| target | state | MAE | bias | target mean |
| --- | --- | ---: | ---: | ---: |
| `Dry_Total_g` | NSW | 18.86 | -0.57 | 70.90 |
| `Dry_Green_g` | NSW | 14.78 | -0.03 | 56.56 |
| `GDM_g` | NSW | 14.75 | 1.36 | 56.69 |
| `Dry_Clover_g` | WA | 11.17 | -1.21 | 22.09 |
| `Dry_Total_g` | Tas | 9.88 | -0.22 | 36.80 |

## 5. Current Baseline Results

Latest saved baseline run:

| model | weighted R2 | MAE | bias |
| --- | ---: | ---: | ---: |
| `extra_trees` | 0.8081 | 6.82 | 0.24 |
| `hgb` | 0.7958 | 7.47 | 0.39 |
| `ridge_log` | 0.6449 | 10.60 | -5.66 |
| `dummy_median` | -0.0376 | 20.45 | 3.62 |

Key baseline findings:

- `extra_trees` is the current best baseline.
- Enforcing `Dry_Total_g = Dry_Green_g + Dry_Dead_g + Dry_Clover_g` improves weighted R2 from `0.80806` to `0.81136`.
- `Dry_Total_g` remains the highest-MAE target, especially in NSW high-biomass examples.
- Image-only color features are much weaker than the current feature set.
- The first EfficientNet-B0 embedding run underperformed the tabular/color baseline, so embeddings remain diagnostic until they improve grouped CV.
- The two-stage zero-inflation check did not improve weighted R2 for `Dry_Clover_g` or `Dry_Dead_g`; keep it diagnostic for now.

## 6. Next Steps

1. Re-run the refined baseline notebook on Kaggle.
   - Confirm that CV selects the best submission-safe feature family.
   - Confirm whether the biomass constraint helps the selected feature family before submission.

2. Run the image-embedding experiment notebook.
   - Use `03_image_embedding_experiments.ipynb` for stronger image features without destabilizing the baseline notebook.
   - Keep pretrained model downloads disabled for scoring-style Kaggle reruns unless weights are attached as an input dataset.

3. Improve embeddings before using them in final submission.
   - Try stronger backbones, lower-dimensional embedding projections, or ridge/boosting models better suited to dense embeddings.
   - Keep embeddings out of the final model unless grouped CV improves.

4. Improve target strategy based on CV output.
   - Keep target-specific models only where they beat the long-format baseline.
   - Keep the biomass accounting constraint as validated post-processing.

5. Tune and blend the strongest tabular/color models.
   - Use `04_tabular_model_tuning.ipynb` to test focused ExtraTrees/HGB configurations and OOF blends.
   - Promote only models that beat the current constrained baseline and preserve hard-segment behavior.

6. Focus error reduction on hard segments.
   - Prioritize NSW high-biomass rows and WA clover rows.
   - Review outliers before treating extreme labels as noise.

7. Strengthen validation.
   - Keep `GroupKFold(image_path)` as the default.
   - Add segment-level reporting by target and state for every experiment.

8. Prepare leaderboard iterations.
   - Track local weighted R2, per-target MAE, and segment error.
   - Submit only changes that improve grouped CV or clearly improve high-priority target behavior.
