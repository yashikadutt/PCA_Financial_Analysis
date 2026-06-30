
import numpy as np

# ── DATASET ──
cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Kolkata',
          'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad']

variables = ['Avg Income', 'Monthly Expenses', 'Savings Rate',
             'Debt-to-Income', 'Financial Stress Index']

#            Income   Expenses  Savings%  DTI%   FSI
raw_data = np.array([
    [55000,  41000,   18,       36,       52],   # Delhi
    [62000,  51000,   12,       55,       71],   # Mumbai
    [72000,  52000,   24,       38,       48],   # Bengaluru
    [38000,  27000,   20,       26,       40],   # Kolkata
    [48000,  35000,   21,       32,       44],   # Chennai
    [58000,  42000,   22,       34,       46],   # Hyderabad
    [54000,  40000,   19,       40,       53],   # Pune
    [42000,  30000,   23,       23,       38],   # Ahmedabad
], dtype=float)

##── STEP 1: Standardize ──
mean = raw_data.mean(axis=0)
std  = raw_data.std(axis=0, ddof=1)
Z = (raw_data - mean) / std

# Print results
print("Mean:", mean)
print("Std Dev:", std)
print("\nStandardized data (Z):")
print(f"{'City':<12}" + "".join(f"{v:>14}" for v in variables))
for i, city in enumerate(cities):
    print(f"{city:<12}" + "".join(f"{Z[i,j]:>14.4f}" for j in range(5)))


## ── STEP 2: Covariance matrix ──
# Measures how each pair of standardized variables varies together.
# Diagonal = variance of each variable (always 1 after standardizing).
# Off-diagonal = correlation strength between two variables.
C = np.cov(Z.T, ddof=1)

print("\nCovariance matrix (C):")
print(f"{'':14}" + "".join(f"{v:>14}" for v in variables))
for j in range(5):
    print(f"{variables[j]:<14}" + "".join(f"{C[j,k]:>14.4f}" for k in range(5)))


## ── STEP 3: Eigen decomposition ──
# Breaks the covariance matrix into eigenvalues and eigenvectors.
# Eigenvectors = new directions (principal components) in the data.
# Eigenvalues = how much variance each direction captures.
eigenvalues, eigenvectors = np.linalg.eigh(C)

print("\nEigenvalues (unsorted):")
print(eigenvalues)

print("\nEigenvectors (unsorted):")
print(eigenvectors)


##── STEP 4: Sort eigenvalues descending ──
# np.linalg.eigh() returns eigenvalues in ascending order by default.
# We reverse this so PC1 (highest variance) comes first, PC2 second, etc.
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print("\nEigenvalues (sorted descending):")
for k in range(5):
    print(f"  λ{k+1} = {eigenvalues[k]:.6f}")

print("\nEigenvectors (sorted, columns = PC1...PC5):")
print(eigenvectors)


#── STEP 5: Explained variance ──
# Converts eigenvalues into percentages so we know how much of the
# total variance each principal component captures.
var_pct = eigenvalues / eigenvalues.sum() * 100
cumvar_pct = np.cumsum(var_pct)

print("\nExplained Variance (%):")
for k in range(5):
    print(f"  PC{k+1}: {var_pct[k]:.2f}%  (cumulative: {cumvar_pct[k]:.2f}%)")


##── STEP 6: Project data onto principal components ──
# Multiplies the standardized data by the sorted eigenvectors.
# Each city now has a "score" on each PC instead of the original 5 variables.
# These scores are uncorrelated and ranked by how much variance they capture.
PC_scores = Z @ eigenvectors

print("\nPCA Scores:")
print(f"{'City':<12}" + "".join(f"{'PC'+str(k+1):>10}" for k in range(5)))
for i, city in enumerate(cities):
    print(f"{city:<12}" + "".join(f"{PC_scores[i,k]:>10.4f}" for k in range(5)))

##── STEP 7: Scree plot ──
# Visualizes how much variance each PC explains, in order.
# Helps decide how many PCs are "enough" to represent the data well.
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.bar(range(1, 6), var_pct, color='#006699')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained (%)')
plt.title('PCA - Scree Plot')
plt.xticks(range(1, 6), [f'PC{k}' for k in range(1, 6)])
plt.savefig('scree_plot.png', dpi=150, bbox_inches='tight')
plt.show()


##── STEP 8: Results summary ──
# Final interpretation: what do the top PCs actually represent,
# and how does each city compare on those dimensions?
print("\n" + "="*50)
print("RESULTS SUMMARY")
print("="*50)

print(f"\nPC1 + PC2 explain {cumvar_pct[1]:.2f}% of total variance")
print("→ Two dimensions are enough to represent this data well.\n")

print("PC1 loadings (which variables drive PC1):")
for j in range(5):
    print(f"  {variables[j]:<22} {eigenvectors[j,0]:>+.4f}")

print("\nPC2 loadings (which variables drive PC2):")
for j in range(5):
    print(f"  {variables[j]:<22} {eigenvectors[j,1]:>+.4f}")

print("\nCity positions (PC1, PC2):")
for i, city in enumerate(cities):
    print(f"  {city:<12} PC1={PC_scores[i,0]:>+7.4f}  PC2={PC_scores[i,1]:>+7.4f}")

##── STEP 9: Biplot (PC1 vs PC2) ──
# Shows both city positions and variable directions on the same plot.
# Arrows = how each variable influences PC1/PC2.
# Dots = where each city lands based on its actual data.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))

scale = 2.5
short_vars = ['Income', 'Expenses', 'Savings', 'DTI', 'FSI']
colors = ['#006699', '#FF6B35', '#27AE60', '#8E44AD', '#E74C3C']

for j in range(5):
    lx = eigenvectors[j, 0] * scale
    ly = eigenvectors[j, 1] * scale
    ax.annotate('', xy=(lx, ly), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=colors[j], lw=2))
    ax.text(lx*1.1, ly*1.1, short_vars[j], fontsize=11, color=colors[j], fontweight='bold')

for i, city in enumerate(cities):
    ax.scatter(PC_scores[i, 0], PC_scores[i, 1], s=150, zorder=5)
    ax.text(PC_scores[i, 0]+0.1, PC_scores[i, 1]+0.1, city, fontsize=10)

ax.axhline(0, color='gray', linewidth=0.8)
ax.axvline(0, color='gray', linewidth=0.8)
ax.set_xlabel(f'PC1 ({var_pct[0]:.1f}%)')
ax.set_ylabel(f'PC2 ({var_pct[1]:.1f}%)')
ax.set_title('PCA Biplot')

plt.savefig('biplot.png', dpi=150, bbox_inches='tight')
plt.show()


##── STEP 10: Loadings heatmap ──
# Shows how strongly each variable loads onto each PC, as a color grid.
# Darker/more intense color = stronger influence (positive or negative).
fig, ax = plt.subplots(figsize=(9, 5))

im = ax.imshow(eigenvectors, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
plt.colorbar(im, ax=ax, label='Loading coefficient')

ax.set_xticks(range(5))
ax.set_xticklabels([f'PC{k+1}' for k in range(5)])
ax.set_yticks(range(5))
ax.set_yticklabels(variables)
ax.set_title('PCA Loadings Heatmap')

for r in range(5):
    for c in range(5):
        val = eigenvectors[r, c]
        color = 'white' if abs(val) > 0.5 else 'black'
        ax.text(c, r, f'{val:.2f}', ha='center', va='center', color=color)

plt.savefig('loadings_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
