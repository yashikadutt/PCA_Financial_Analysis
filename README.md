# PCA-Financial-Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![Finance](https://img.shields.io/badge/Quantitative%20Finance-00599C?style=for-the-badge&logo=chartdotjs&logoColor=white)

---

## 📌 Overview

A Python implementation of **Principal Component Analysis** on financial indicators across **8 major Indian cities** (2023–24 data).

Reduces 5 correlated financial variables — income, expenses, savings rate, debt-to-income, and a composite financial stress index — into 2 principal components that together explain **99.45% of total variance**, then validates the manual eigen-decomposition against scikit-learn's PCA implementation.

Originally developed as a supervised summer project (BSP-156, USBAS, GGSIPU) — manual PCA was first implemented in Excel and validated in MATLAB. This repository reimplements the full pipeline in Python.

---

## ⚙️ Methods Implemented

| Step | Description |
|---|---|
| **Standardization** | Z-score normalization (ddof=1, matches Excel's `STDEV.S`) so variables on different scales (₹ vs %) are comparable |
| **Covariance Matrix** | Measures co-movement between all variable pairs post-standardization |
| **Eigen Decomposition** | Extracts eigenvalues (variance captured) and eigenvectors (component directions) via `np.linalg.eigh` |
| **Variance Explained** | Eigenvalues converted to % and ranked to identify how many components are needed |
| **PCA Scores** | Projects each city onto the new principal component space |
| **sklearn Validation** | Cross-checks manual results against `sklearn.decomposition.PCA` |

---

## 📊 Results

### Variance Explained

| Component | Eigenvalue | % Variance | Cumulative % |
|---|---|---|---|
| PC1 | 3.7877 | 75.75% | 75.75% |
| PC2 | 1.1846 | 23.69% | 99.45% |
| PC3–PC5 | 0.0277 | 0.55% | 100.00% |

> PC1 and PC2 together capture nearly all the variance in the original 5 variables — a textbook PCA result confirming strong correlation structure in the dataset.

### Component Interpretation

**PC1 — "Financial Pressure" axis**
Driven by Income (−0.40), Expenses (−0.46), Debt-to-Income (−0.51), and Financial Stress Index (−0.49), opposed by Savings Rate (+0.36). Cities scoring negative on PC1 have higher cost-of-living and debt burden; cities scoring positive have comparatively stronger savings relative to spending.

| City | PC1 Score | Interpretation |
|---|---|---|
| Mumbai | −3.69 | Highest cost & debt burden |
| Bengaluru | −0.99 | Above-average pressure |
| Ahmedabad | +2.40 | Lowest cost & debt burden |
| Kolkata | +2.16 | Strong relative savings |

**PC2 — Savings/Income axis**
Driven primarily by Savings Rate (−0.66) and Income (−0.57). Bengaluru is the standout outlier (PC2 = −2.23), driven by the combination of the highest savings rate (24%) and high income in the dataset.

---

## 📈 Visualizations

**Scree Plot** — variance explained per principal component
`plot1_scree.png`

**Biplot** — city positions and variable loading directions on PC1 vs PC2
`plot2_biplot.png`

**Loadings Heatmap** — full loading matrix across all 5 components
`plot3_loadings_heatmap.png`

---

## 🚀 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python pca_analysis.py
```

---

## 🗂️ Project Structure

```
PCA-Financial-Analysis/
├── pca_analysis.py
├── requirements.txt
├── plot1_scree.png
├── plot2_biplot.png
├── plot3_loadings_heatmap.png
└── README.md
```

---

## 🔑 Key Concepts

**Principal Component Analysis** — A dimensionality reduction technique that transforms correlated variables into a smaller set of uncorrelated components, ranked by how much variance they explain.

**Eigenvalues & Eigenvectors** — Eigenvectors define the direction of each new component; eigenvalues quantify how much of the data's total variance lies along that direction.

**Standardization** — Required before PCA whenever variables are on different scales (here, rupees vs percentages), since PCA is variance-based and would otherwise be dominated by whichever variable has the largest raw magnitude.

**Limitation** — The dataset covers 8 major Indian cities, sized to balance genuinely sourced, city-level financial data (Statista, CNBC) against the limited public availability of consistent metrics at this granularity. A larger sample would strengthen statistical generalization, but at the cost of relying on estimated rather than sourced figures for additional cities.

---

