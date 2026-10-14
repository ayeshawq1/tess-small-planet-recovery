# Optimal Preprocessing Prediction for Small-Planet Recovery in TESS Light Curves

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23058593.svg)](https://doi.org/10.5281/zenodo.23058593)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This repository contains the full analysis, notebooks, configuration files, frozen outputs, figures, and manuscript materials for a controlled injection-recovery study of small transiting planets in TESS light curves.

The project began by testing how preprocessing choices, stellar variability, signal strength, and transit-search method affect recovery. It was then extended into a predictive framework that asks a more practical question:

> Can we predict, before running a full transit search, which preprocessing strategy is most likely to maximize small-planet recovery for a given TESS light curve?

The study uses real TESS photometry, synthetic transit injections, multiple preprocessing strategies, frozen search protocols, and an out-of-sample heldout evaluation.

---

## Main Result

The final learned preprocessing recommender was evaluated on 20 previously unseen TESS host stars using 1,200 small-planet injections.

Exact-period recovery on the heldout set was:

- **Random Forest recommender:** 415 / 1200 = **34.58%**
- **ADAPT-v1:** 386 / 1200 = **32.17%**
- **TRAIN-selected fixed baseline:** 317 / 1200 = **26.42%**
- **Oracle upper reference:** 451 / 1200 = **37.58%**

The learned model therefore improved exact-period recovery by:

- **+2.42 percentage points over ADAPT-v1**
- **+8.17 percentage points over the TRAIN-selected fixed strategy**

A 10,000-resample host-aware bootstrap gave:

- Random Forest vs ADAPT-v1: **95% CI = -1.17 to +6.67 percentage points**
- Random Forest vs fixed baseline: **95% CI = +1.17 to +16.25 percentage points**

The main scientific conclusion is that preprocessing should not necessarily be treated as a single fixed step applied identically to every TESS target. Host-dependent preprocessing can improve small-planet recovery, and part of that decision can be learned from light-curve properties available before the transit search.

---

## Study Design

The analysis uses:

- real TESS light curves
- controlled synthetic transit injections
- a frozen Box Least Squares search pipeline
- four preprocessing strategies:
  - `BASELINE`
  - `SG_101`
  - `SG_301`
  - `SG_501`
- experimentally generated host-level preprocessing labels
- supervised models including:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - Gradient Boosting
  - a compact neural network
- frozen TRAIN / VALIDATION / HELDOUT splits
- host-aware bootstrap uncertainty estimation

The final dataset contains:

- **100 TESS host stars**
- **60 TRAIN**
- **20 VALIDATION**
- **20 HELDOUT**
- **12,000 unique transit injections**
- **48,000 preprocessing-method evaluations**

The final HELDOUT experiment contains:

- **2,400 unique injected signals**
- **9,600 paired preprocessing/search evaluations**
- **1,200 primary small-planet injections**

---

## Validation Strategy

The project was designed around a frozen evaluation protocol.

Model and preprocessing decisions were made using the TRAIN and VALIDATION sets only. The final preprocessing recommender was frozen before the HELDOUT outcomes were evaluated.

The primary endpoint is:

> **Exact recovery of the injected orbital period within the predefined tolerance.**

Aliases at half and double the injected period are tracked separately as secondary outcomes.

No post-heldout model tuning, feature selection, threshold tuning, preprocessing changes, or label changes were performed.

---

## Final Model

The Random Forest was selected because it achieved the highest downstream exact-period recovery on the validation set.

Validation small-planet exact recovery:

- Random Forest: **39.67%**
- SG501 / ADAPT-v1: **39.50%**
- Gradient Boosting: **38.67%**
- Decision Tree: **37.17%**
- Neural Network: **33.25%**
- Logistic Regression: **30.08%**

The Random Forest was then frozen and applied to the 20 heldout hosts.

---

## Figures

The repository includes the final publication figures:

1. **Heldout exact-period recovery comparison**
2. **Per-host recovery across the heldout sample**
3. **Host-aware bootstrap uncertainty**
4. **Random Forest preprocessing recommendations vs heldout oracle**

These figures are used in the final manuscript.

---

## Manuscript

The final manuscript is included in the `paper/` directory.

**Title:**

**Optimal Preprocessing Prediction for Small-Planet Recovery in TESS Light Curves**

The repository includes:

- final PDF
- LaTeX source
- publication figures
- frozen result tables
- analysis notebook

---

## Reproducibility

The analysis is designed to preserve the distinction between model development and final evaluation.

Important frozen components include:

- preprocessing definitions
- injection grid
- BLS search configuration
- recovery criteria
- feature set
- model-selection rule
- ADAPT-v1 threshold
- TRAIN-selected fixed benchmark
- heldout host split

The final heldout run completed:

- **2400 / 2400 cases**
- **9600 / 9600 method rows**
- **0 failed rows**
- perfect four-method pairing

---

## Generative AI Disclosure

OpenAI ChatGPT was used under human supervision for code debugging, visualization refinement, and manuscript editing. All analyses were executed on the project data, and all numerical results, figures, and scientific interpretations were checked and approved by the author.

---

## Data and Code Availability

All code, notebooks, figures, configuration files, and frozen result tables required to inspect the analysis are included in this repository.

A versioned archival release is available through Zenodo:

**DOI:** https://doi.org/10.5281/zenodo.23058593

---

## Author

**Ayesha Waqas**  
Independent Researcher

---

## License

This repository is released under the **MIT License**.
