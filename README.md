# Optimal Preprocessing Prediction for Small-Planet Recovery in TESS Light Curves

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23373425.svg)](https://doi.org/10.5281/zenodo.23373425)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This repository contains the complete analysis, notebooks, configuration files, frozen outputs, figures, and manuscript materials for a controlled injection-recovery study of small transiting planets in TESS light curves.

The project investigates whether the preprocessing strategy applied to a TESS light curve can be selected adaptively before running a full transit search.

The central research question is:

> Can we predict, before running a full transit search, which preprocessing strategy is most likely to maximize small-planet recovery for a given TESS light curve?

The study uses real TESS photometry, controlled synthetic transit injections, multiple preprocessing strategies, a frozen transit-search protocol, supervised machine-learning models, and a final out-of-sample heldout evaluation.

---

## Main Result

The final learned preprocessing recommender was evaluated on 20 previously unseen TESS host stars using 1,200 primary small-planet injections.

Exact-period recovery on the heldout set was:

- **Random Forest recommender:** 415 / 1200 = **34.58%**
- **ADAPT-v1:** 386 / 1200 = **32.17%**
- **TRAIN-selected fixed baseline:** 317 / 1200 = **26.42%**
- **Oracle upper reference:** 451 / 1200 = **37.58%**

The Random Forest improved exact-period recovery by:

- **+2.42 percentage points over ADAPT-v1**
- **+8.17 percentage points over the TRAIN-selected fixed strategy**

A 10,000-resample host-aware bootstrap gave:

- Random Forest vs ADAPT-v1: **95% CI = -1.17 to +6.67 percentage points**
- Random Forest vs fixed baseline: **95% CI = +1.17 to +16.25 percentage points**

The strongest conclusion is that preprocessing should not necessarily be treated as a single fixed operation applied identically to every TESS target. Host-dependent preprocessing can improve small-planet recovery, and part of that decision can be predicted from light-curve properties available before the transit search.

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

The final heldout experiment contains:

- **2,400 unique injected signals**
- **9,600 paired preprocessing/search evaluations**
- **1,200 primary small-planet injections**

---

## Preprocessing Strategies

Four preprocessing choices were evaluated:

### BASELINE

The reference preprocessing configuration used as the fixed comparison method.

### SG_101

Savitzky-Golay detrending with a 101-point window.

### SG_301

Savitzky-Golay detrending with a 301-point window.

### SG_501

Savitzky-Golay detrending with a 501-point window.

The purpose of the study was not to assume one of these strategies was universally optimal, but to test whether the best choice could vary from star to star and whether that variation could be predicted.

---

## Transit Injection and Search

Synthetic transit signals were injected into real TESS light curves using a fixed experimental protocol.

The transit-search pipeline used a frozen Box Least Squares configuration.

The primary scientific endpoint was:

> **Exact recovery of the injected orbital period within the predefined tolerance.**

Half-period and double-period aliases were tracked separately as secondary outcomes.

The injected truth was not passed into the search algorithm.

---

## Development and Heldout Protocol

The project used a strict development and heldout workflow.

Model development and preprocessing decisions were made using the TRAIN and VALIDATION sets only.

The following components were frozen before the final heldout evaluation:

- preprocessing definitions
- injection grid
- BLS search configuration
- recovery criteria
- feature set
- model-selection rule
- ADAPT-v1 threshold
- TRAIN-selected fixed benchmark
- heldout host split
- final model choice

No post-heldout:

- model tuning
- feature selection
- threshold tuning
- preprocessing changes
- label changes

were performed.

---

## Machine-Learning Models

The following models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- Compact Keras multilayer perceptron

Model selection was based primarily on downstream exact-period recovery on the validation set rather than classification accuracy alone.

Validation small-planet exact recovery:

- **Random Forest:** 39.67%
- **SG501 / ADAPT-v1:** 39.50%
- **Gradient Boosting:** 38.67%
- **Decision Tree:** 37.17%
- **Neural Network:** 33.25%
- **Logistic Regression:** 30.08%

The Random Forest was therefore frozen as the final learned preprocessing recommender.

---

## Heldout Evaluation

The final Random Forest was evaluated on 20 unseen TESS host stars.

The heldout experiment completed successfully with:

- **2400 / 2400 cases**
- **9600 / 9600 method rows**
- **0 failed rows**
- perfect four-method pairing

Primary heldout exact-period recovery:

| Strategy | Exact recoveries | Recovery |
|---|---:|---:|
| TRAIN-selected fixed baseline | 317 / 1200 | 26.42% |
| ADAPT-v1 | 386 / 1200 | 32.17% |
| Random Forest | 415 / 1200 | 34.58% |
| Oracle | 451 / 1200 | 37.58% |

The frozen Random Forest satisfied the predeclared heldout success criterion by outperforming both prespecified deployable benchmarks on the observed heldout sample.

---

## Host-Aware Uncertainty

Because multiple injected signals were generated for each star, uncertainty was estimated by resampling entire host stars rather than individual injections.

Across 10,000 host-level bootstrap resamples:

### Random Forest vs ADAPT-v1

- observed difference: **+2.42 percentage points**
- 95% percentile interval: **-1.17 to +6.67 percentage points**
- Random Forest exceeded ADAPT-v1 in **88.81%** of bootstrap resamples

### Random Forest vs TRAIN-selected fixed baseline

- observed difference: **+8.17 percentage points**
- 95% percentile interval: **+1.17 to +16.25 percentage points**
- Random Forest exceeded the fixed strategy in **99.01%** of bootstrap resamples

The evidence is therefore stronger for improvement over globally fixed preprocessing than for superiority over the simpler ADAPT-v1 rule.

---

## Oracle Comparison

A non-deployable oracle was used as an upper reference.

The oracle selected the best-performing preprocessing method separately for each heldout host using observed recovery outcomes.

Oracle exact-period recovery:

**451 / 1200 = 37.58%**

Random Forest exact-period recovery:

**415 / 1200 = 34.58%**

The learned model therefore finished **3.00 percentage points below the oracle**.

The Random Forest matched the oracle's exact preprocessing choice on:

**9 / 20 heldout hosts = 45%**

Despite this modest categorical agreement, downstream recovery was much closer to the oracle, showing that classification agreement alone does not fully capture scientific utility.

---

## Figures

The repository includes the final publication figures:

1. **Heldout Small-Planet Recovery**
2. **Recovery Performance Across Individual Heldout Stars**
3. **Host-Aware Bootstrap Uncertainty**
4. **Recommended Preprocessing vs Heldout Oracle**

These figures correspond directly to the final heldout analysis reported in the manuscript.

---

## Manuscript

The final manuscript is included in the `paper/` directory.

**Title:**

**Optimal Preprocessing Prediction for Small-Planet Recovery in TESS Light Curves**

The paper materials include:

- final PDF
- LaTeX source
- publication figures
- frozen result tables
- analysis notebook

---

## Repository Structure

A typical structure is:

```text
tess-small-planet-recovery/
├── README.md
├── LICENSE
├── paper/
│   ├── tess_preprocessing_paper_optimal_preprocessing_prediction_final.pdf
│   ├── tess_preprocessing_paper_optimal_preprocessing_prediction_nodraft.tex
│   └── figures/
├── notebooks/
│   └── TESS_Project.ipynb
├── results/
│   └── phase2/
│       ├── objective_09/
│       └── objective_10_final_figures/
├── configs/
│   └── phase2/
└── ...
