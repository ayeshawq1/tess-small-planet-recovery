[README.md](https://github.com/user-attachments/files/32846790/README.md)
# TESS Small-Planet Recovery

Injection-recovery benchmarking of small transiting planets in TESS light curves, including preprocessing bias, BLS vs TLS, adaptive preprocessing, held-out evaluation, and real TOI case studies.

## Overview

This repository contains the code, notebooks, configuration files, frozen result tables, figures, and manuscript materials for a controlled study of small-planet recovery in TESS light curves.

The central research question is:

> How do preprocessing choices, stellar variability, signal strength, and search method change the recovery of small transiting planets in TESS light curves, and can a simple adaptive preprocessing rule improve recovery without increasing spurious detections?

The project uses real TESS light curves, synthetic transit injection, blind period searches, paired preprocessing experiments, BLS/TLS comparisons, development-only method tuning, and a frozen held-out evaluation.

## Main findings

- The frozen baseline recovered **622/1000 injections (62.2%)** exactly.
- A fixed Savitzky-Golay configuration, **SG_501**, increased development exact-period recovery to **73.3%**, but also increased transit-depth suppression.
- On a matched 200-case subset, **BLS recovered 64.0%** exactly and **TLS recovered 63.0%**, while TLS was about **9.5× slower** in median runtime.
- The frozen adaptive rule, **ADAPT-v1**, used robust light-curve RMS to choose between the baseline and SG_501 preprocessing.
- On development data, small-planet exact recovery increased from **45.5% to 64.5%**.
- On the untouched held-out benchmark, small-planet exact recovery increased from **74.17% to 83.75%**, an absolute improvement of **9.58 percentage points**.
- The held-out gain was concentrated in the single higher-variability host for which ADAPT-v1 selected SG_501.
- Across all held-out injections, exact recovery increased from **89.0% to 92.33%**.
- Three real TOI case studies were evaluated blindly after freezing the pipeline; none recovered the archive period within 1%, highlighting the difference between controlled injection-recovery performance and blind performance on real systems.

## Scientific caution

The project is intentionally conservative about interpretation.

- A BLS top period is not treated as a planet detection.
- No binary false-positive rate is claimed from BLS SDE because no binary SDE threshold was frozen.
- Odd-even and secondary-eclipse checks are treated as vetting evidence, not confirmation.
- Apparent radius estimates based on `sqrt(depth)` are diagnostic approximations, not full physical planet-radius inference.
- The held-out sample contains only three host stars.
- Real TOI analyses are illustrative case studies and are not independent planet confirmations.

## Pipeline

The workflow was built and frozen in stages:

1. Retrieve real TESS SPOC light curves.
2. Apply quality filtering and median normalization.
3. Run blind Box Least Squares searches.
4. Validate the baseline on known transiting planets.
5. Freeze `baseline_v1`.
6. Inject synthetic transits using BATMAN.
7. Define deterministic recovery and alias rules.
8. Run the 1,000-case baseline completeness benchmark.
9. Compare paired preprocessing variants.
10. Compare BLS and TLS on identical injected cases.
11. Build and ablate ADAPT-v1 using development hosts only.
12. Freeze the adaptive rule and primary metric.
13. Run the untouched held-out evaluation once.
14. Apply the frozen pipeline to real TOI case studies.
15. Freeze final tables, figures, and manuscript outputs.

## Baseline search configuration

The frozen BLS configuration uses:

- Period range: **0.5–15 days**
- Transit durations: **1, 1.5, 2, 2.5, 3, 4, and 5 hours**
- Minimum number of transits: **2**
- BLS oversample: **10**
- Primary recovery: top-period exact recovery within **1%**
- Explicit alias handling for **P/2** and **2P**

The baseline preprocessing is deliberately minimal:

- SPOC light curves
- PDCSAP flux preferred
- `QUALITY == 0`
- finite-value filtering
- median normalization
- no outlier removal
- no detrending

## Known-planet validation

The frozen baseline was validated on five known systems using the same configuration for every target:

| Target | Reference period (days) | Recovery class |
|---|---:|---|
| WASP-18 | 0.941452 | EXACT |
| WASP-19 | 0.788839 | EXACT |
| WASP-43 | 0.813475 | EXACT |
| WASP-121 | 1.274925 | EXACT |
| WASP-4 | 1.338231 | EXACT |

This validation also revealed an important failure mode: aggressive smoothing could preserve the recovered period while substantially suppressing transit depth.

## Transit injection

Synthetic transits are injected into real TESS noise using **BATMAN**.

The injection stage is intentionally separated from the search stage so that injected truth is never passed into the blind period search.

The frozen injection design spans:

- orbital periods: **1, 3, 6, 10 days**
- radius ratios: **0.015, 0.025, 0.040, 0.060, 0.090**
- repeated random epochs and impact parameters
- multiple development host stars

Random seeds and injection IDs are saved for reproducibility.

## Preprocessing benchmark

Four preprocessing variants were compared on identical injections:

| Method | Exact recovery | Median depth bias | Median apparent-radius bias |
|---|---:|---:|---:|
| BASELINE | 0.622 | -0.084 | -0.043 |
| SG_101 | 0.510 | -0.865 | -0.633 |
| SG_301 | 0.691 | -0.564 | -0.340 |
| SG_501 | 0.733 | -0.385 | -0.216 |

The main result is a clear tradeoff: preprocessing can improve period recovery while biasing transit depth and apparent radius.

## BLS vs TLS

BLS and Transit Least Squares were compared on the same 200 injected cases and the same period range.

| Search method | Exact recovery | Alias-aware recovery | Median runtime |
|---|---:|---:|---:|
| BLS | 0.640 | 0.640 | 3.38 s |
| TLS | 0.630 | 0.640 | 32.13 s |

In this benchmark, TLS did not improve exact recovery enough to justify its substantially larger runtime cost.

## ADAPT-v1

ADAPT-v1 is a deterministic preprocessing rule based only on robust light-curve RMS.

```text
if robust_rms <= 2.15e-4:
    use BASELINE
else:
    use SG_501
```

The rule does not use injected period, depth, radius, or any other injected truth.

Development ablation:

| Method | Overall exact recovery | Small-planet exact recovery |
|---|---:|---:|
| FIXED_BASELINE | 0.622 | 0.455 |
| FIXED_SG501 | 0.733 | 0.588 |
| ADAPT_V1 | 0.763 | 0.645 |
| REVERSE_RULE | 0.592 | 0.398 |

ADAPT-v1 was frozen before opening the held-out data.

## Held-out evaluation

The final held-out benchmark used three untouched host stars and **600 unique injections**.

Primary metric: exact-period recovery for injections with `Rp/Rstar <= 0.025`.

| Method | Recovered | Attempted | Completeness |
|---|---:|---:|---:|
| FIXED_BASELINE | 178 | 240 | 0.7417 |
| ADAPT_V1 | 201 | 240 | 0.8375 |

Absolute improvement: **+0.0958**.

Paired outcomes:

- baseline miss → ADAPT recovery: **24**
- baseline recovery → ADAPT miss: **1**
- both recovered: **177**
- both missed: **38**

The host-aware bootstrap 95% interval for the primary difference was **[0.0000, 0.2875]**.

Across all 600 held-out injections:

- FIXED_BASELINE exact recovery: **0.8900**
- ADAPT_V1 exact recovery: **0.9233**

The improvement was concentrated in the higher-variability held-out host where ADAPT-v1 selected SG_501.

## Real TOI case studies

Three TOI case studies were selected under a written rule before running the frozen pipeline. Blind pipeline outputs were saved before archive comparison.

None of the three recovered the archive period within 1%.

These cases are preserved as negative results rather than retuned away. They illustrate the gap between controlled injection-recovery performance and blind analysis of real systems.

## Repository structure

A recommended layout is:

```text
tess-small-planet-recovery/
│
├── README.md
├── requirements_tess_project.txt
├── environment.yml
│
├── notebooks/
│   └── TESS_Project_Clean_PC_Objectives_1_to_8.ipynb
│
├── src/
│   ├── data.py
│   ├── preprocess.py
│   ├── search.py
│   ├── evaluate.py
│   └── vet.py
│
├── configs/
│   ├── baseline_v1.json
│   ├── week14_adapt_v1/
│   ├── week15_heldout/
│   └── week16_final/
│
├── results/
│   ├── week11/
│   ├── week12/
│   ├── week13/
│   ├── week14/
│   ├── week15_heldout/
│   ├── week15_real_case_studies/
│   └── week16_final/
│
├── figures/
│   ├── week11/
│   ├── week12/
│   ├── week13/
│   ├── week14/
│   ├── week15_heldout/
│   └── week16_final/
│
├── tests/
│
└── paper/
    ├── main.tex
    └── figures/
```

Your exact local folder structure may differ. The important reproducibility requirement is that frozen configs, result tables, and final figures remain traceable to the code that produced them.

## Installation

Python 3.11 was used for the final local workflow.

Example Conda setup:

```bash
conda create -n tess-project python=3.11 -y
conda activate tess-project
python -m pip install -r requirements_tess_project.txt
```

Core dependencies include:

- NumPy
- pandas
- Matplotlib
- SciPy
- Astropy
- Lightkurve
- Astroquery
- BATMAN
- Transit Least Squares
- Joblib
- JupyterLab
- pytest

## Running the analysis

The safest way to reproduce the project is to follow the frozen order rather than rerunning later experiments independently:

```text
baseline validation
    ↓
injection engine
    ↓
recovery evaluator
    ↓
Week 11 benchmark
    ↓
Week 12 preprocessing comparison
    ↓
Week 13 BLS/TLS comparison
    ↓
Week 14 ADAPT-v1 development + freeze
    ↓
Week 15 held-out evaluation
    ↓
Week 15B case studies
    ↓
Week 16 final figures/tables
```

Do not modify the ADAPT-v1 threshold or preprocessing rule and then compare the modified version against the existing held-out result. That would break the development/held-out separation used in the study.

## Reproducibility safeguards

The project preserves several safeguards against result leakage and silent retuning:

- deterministic seeds
- frozen configs
- explicit development and held-out host sets
- saved hash manifests for frozen ADAPT-v1 source/config
- identical injection IDs across paired preprocessing methods
- archive values withheld until after blind real-target outputs were saved
- failed and negative results preserved
- no post-held-out retuning

## Paper

The repository accompanies the manuscript:

**How Small a Planet Can TESS Really See? Preprocessing, Stellar Variability, Search Algorithms, and Adaptive Transit Recovery in TESS Light Curves**

The paper includes the full experimental design, quantitative results, limitations, and real-target case studies.

## Main limitations

The conclusions should be interpreted within the scope of this experiment:

1. The held-out evaluation contains only three host stars.
2. Only one held-out host crossed the ADAPT-v1 RMS threshold and therefore received SG_501.
3. Savitzky-Golay window lengths are specified in sample counts, so the corresponding physical timescale depends on cadence.
4. Transit-depth and apparent-radius estimates are simplified diagnostics.
5. No frozen binary detection threshold was established for BLS SDE.
6. Injection recovery does not guarantee successful blind recovery on real planetary systems.
7. The results characterize this sample and pipeline rather than all TESS observations.

## Citation

If you use this repository, please cite the accompanying manuscript. A BibTeX entry can be added here after the paper has a stable arXiv identifier or DOI.

```bibtex
@article{tess_small_planet_recovery,
  title   = {How Small a Planet Can TESS Really See? Preprocessing, Stellar Variability, Search Algorithms, and Adaptive Transit Recovery in TESS Light Curves},
  author  = {Ayesha Waqas},
  year    = {2026},
  note    = {Preprint}
}
```

## References

Core references used in the project include:

- Ricker et al. (2015), *Transiting Exoplanet Survey Satellite (TESS)*.
- Kovács, Zucker, & Mazeh (2002), *A box-fitting algorithm in the search for periodic transits*.
- Kreidberg (2015), *BATMAN: BAsic Transit Model cAlculatioN in Python*.
- Hippke & Heller (2019), *Optimized transit detection algorithm to search for periodic transits of small planets*.
- NASA Exoplanet Archive.
- MAST / TESS SPOC data products.

## License

Add the license you want to use before making the repository public. For research code, an MIT or BSD-3-Clause license is a common choice.

---

This repository preserves the full research trail, including development choices, frozen protocols, negative results, and the final held-out evaluation.
