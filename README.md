# PCA-Financial-Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)

Five financial indicators across 8 Indian cities — income, expenses, savings rate, debt-to-income, and a financial stress index — turn out to be almost the same number wearing different units. This project shows that, and quantifies it.

---

## The question

Income, expenses, debt-to-income, and financial stress are usually treated as separate things to track. But are they actually independent, or is a city that earns more also spending more, borrowing more, and stressed more — just one underlying pattern measured five different ways?

## What the data says

Computing the correlation matrix first answers this directly: Income and Expenses move together at **r = 0.97**. Debt-to-Income and Financial Stress Index move together at **r = 0.98**. Almost nothing here is independent.

That's confirmed by the PCA result — one single axis (PC1) absorbs **75.75%** of all variance across the 5 variables, and a second axis picks up nearly everything else (**23.69%**). Two numbers per city replace five, losing almost no information.

| Component | Variance Explained | Cumulative |
|---|---|---|
| PC1 | 75.75% | 75.75% |
| PC2 | 23.69% | 99.45% |
| PC3, PC4, PC5 | 0.55% combined | 100.00% |

## What PC1 actually is

It's not an abstract math construct — its loadings spell out a recognisable axis:

```
Income            -0.40
Expenses          -0.46
Debt-to-Income    -0.51
Financial Stress  -0.49
Savings Rate      +0.36
```

Four variables pulling one way, Savings Rate pulling the other. PC1 is a **cost-of-living-and-debt-burden score**, derived rather than assumed:

| City | PC1 Score | Reading |
|---|---|---|
| Mumbai | −3.69 | Highest income, highest debt burden, lowest relative savings |
| Bengaluru | −0.99 | Moderately high pressure |
| Kolkata | +2.16 | Low cost, comparatively strong savings |
| Ahmedabad | +2.40 | Lowest cost, lowest debt burden |

PC2 picks up what PC1 misses: Bengaluru is the one outlier (PC2 = −2.23) — high income *and* the highest savings rate in the dataset (24%), a profile distinct from every other city.

## Pipeline

`pca_analysis.py` implements PCA from the ground up, then checks it against `scikit-learn`:

1. Standardise (z-score, ddof=1 — matches Excel's `STDEV.S`, used to keep this consistent with the original manual version of this project)
2. Covariance matrix of the standardised data
3. Eigendecomposition via `np.linalg.eigh`
4. Sort eigenvalues/eigenvectors descending
5. Project standardised data onto the sorted eigenvectors → PCA scores
6. Cross-check every number against `sklearn.decomposition.PCA`

No step is hidden behind a library call until step 6 — the manual implementation is the actual analysis; sklearn is there to prove it's correct, not to replace it.

## Visuals

![Scree Plot](scree_plot.png)
*Two components, not five — the scree plot is the visual version of the correlation argument above.*

![Biplot](biplot.png)
*Arrows show how each variable pulls; dots show where each city actually lands. Mumbai and Ahmedabad sit at opposite ends of the same axis.*

![Loadings Heatmap](loadings_heatmap.png)
*Full loading matrix — confirms PC3 onward carry almost no signal (near-zero coefficients).*

## Run it

```bash
pip install -r requirements.txt
python pca_analysis.py
```

## On the dataset

8 cities, sourced from Statista (city-wise average salaries) and CNBC (EMI-to-income ratios by metro). City-level financial data at this granularity isn't published consistently across more cities in India — extending this to 15-20 cities would mean estimating rather than sourcing most of the additional numbers, which would weaken rather than strengthen the analysis. 8 honest data points beat 20 invented ones.

This project began as a manual Excel + MATLAB analysis (BSP-156, supervised by Prof. Rashmi Bhardwaj, USBAS, GGSIPU). This repository is the from-scratch Python rebuild of that same methodology.

---

**Yashika Dutt** 


