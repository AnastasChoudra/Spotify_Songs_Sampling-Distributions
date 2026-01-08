from helper_functions import choose_statistic, population_distribution, sampling_distribution
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os

# ============================================================================
# SPOTIFY TEMPO SAMPLING DISTRIBUTIONS ANALYSIS
# ============================================================================
# This script analyzes the tempo distribution of Spotify songs and demonstrates
# the Central Limit Theorem through sampling distribution analysis.
# ============================================================================

# Create figures directory if it doesn't exist
figures_dir = 'figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
    print(f"Created '{figures_dir}' directory for saving visualizations")

# Load the Spotify dataset from CSV file
spotify_data = pd.read_csv('genres_v2.csv')
print("Dataset loaded successfully!")
print(spotify_data.head())
print(f"\nDataset shape: {spotify_data.shape}")

# Extract tempo column for analysis
# Tempo is measured in beats per minute (bpm)
song_tempos = spotify_data.tempo

# ============================================================================
# SECTION 1: DATA QUALITY CHECKS
# ============================================================================
# Verify data integrity before performing statistical analysis
print("\n" + "="*60)
print("DATA QUALITY CHECKS")
print("="*60)
print(f"Missing values: {song_tempos.isna().sum()}")
print(f"Data type: {song_tempos.dtype}")
print(f"Total songs in dataset: {len(song_tempos)}")

# ============================================================================
# SECTION 2: DESCRIPTIVE STATISTICS
# ============================================================================
# Calculate central tendency, spread, and shape measures for the population
print("\n" + "="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)
population_mean = np.mean(song_tempos)
population_std = np.std(song_tempos)
population_median = np.median(song_tempos)
q1 = np.percentile(song_tempos, 25)
q3 = np.percentile(song_tempos, 75)
iqr = q3 - q1
skewness = stats.skew(song_tempos)  # Measures asymmetry: 0=symmetric, <0=left-skewed, >0=right-skewed
kurtosis = stats.kurtosis(song_tempos)  # Measures tail heaviness: 0=normal, >0=heavy tails, <0=light tails

print(f"Mean: {population_mean:.2f} bpm")
print(f"Median: {population_median:.2f} bpm")
print(f"Std Dev: {population_std:.2f}")
print(f"Min: {np.min(song_tempos):.2f} bpm")
print(f"Max: {np.max(song_tempos):.2f} bpm")
print(f"Q1 (25th percentile): {q1:.2f} bpm")
print(f"Q3 (75th percentile): {q3:.2f} bpm")
print(f"IQR (Interquartile Range): {iqr:.2f}")
print(f"Skewness: {skewness:.4f}")
print(f"Kurtosis: {kurtosis:.4f}")

# ============================================================================
# SECTION 3: CONFIDENCE INTERVALS
# ============================================================================
# Calculate 95% and 99% confidence intervals using t-distribution
# These intervals estimate where the true population mean likely falls
print("\n" + "="*60)
print("CONFIDENCE INTERVALS FOR POPULATION MEAN")
print("="*60)
ci_95 = stats.t.interval(0.95, len(song_tempos)-1, loc=population_mean, scale=stats.sem(song_tempos))
ci_99 = stats.t.interval(0.99, len(song_tempos)-1, loc=population_mean, scale=stats.sem(song_tempos))
print(f"95% Confidence Interval: [{ci_95[0]:.2f}, {ci_95[1]:.2f}] bpm")
print(f"99% Confidence Interval: [{ci_99[0]:.2f}, {ci_99[1]:.2f}] bpm")

# ============================================================================
# SECTION 4: SAMPLING DISTRIBUTIONS & CENTRAL LIMIT THEOREM
# ============================================================================
# Demonstrates CLT by examining how sample statistics vary across different samples
print("\n" + "="*60)
print("SAMPLING DISTRIBUTIONS")
print("="*60)

# Visualize the population distribution of tempos
print("\nGenerating population distribution...")
population_distribution(song_tempos, figures_dir)

# Show how sample means vary (demonstrates CLT - sample means are normally distributed)
print("Generating sampling distribution of the mean...")
sampling_distribution(song_tempos, 30, 'Mean', figures_dir)

# Analyze minimum values across samples (less commonly used but shows different statistic behavior)
print("Generating sampling distribution of the minimum...")
sampling_distribution(song_tempos, 30, 'Minimum', figures_dir)

# Examine variance across samples (useful for understanding sample variability)
print("Generating sampling distribution of the variance...")
sampling_distribution(song_tempos, 30, 'Variance', figures_dir)

# ============================================================================
# SECTION 5: STANDARD ERROR & SAMPLING STATISTICS
# ============================================================================
# Calculate standard error which measures how much sample means vary from population mean
sample_size = 30
standard_error = population_std / np.sqrt(sample_size)
print(f"\nSample size: {sample_size}")
print(f"Standard error of the mean: {standard_error:.2f} bpm")
print(f"(Smaller standard error = more precise sample estimates)")

# ============================================================================
# SECTION 6: PROBABILITY CALCULATIONS
# ============================================================================
# Use the normal distribution to calculate probabilities about sample means
# These probabilities are based on the Central Limit Theorem
print("\n" + "="*60)
print("PROBABILITY ANALYSIS (Normal Distribution)")
print("="*60)

# Probability that a sample mean is at or below 140 bpm
prob_140 = stats.norm.cdf(140, population_mean, standard_error) * 100
print(f"P(sample mean ≤ 140 bpm): {prob_140:.2f}%")

# Probability that a sample mean is at or above 150 bpm
prob_150 = (1 - stats.norm.cdf(150, population_mean, standard_error)) * 100
print(f"P(sample mean ≥ 150 bpm): {prob_150:.2f}%")

# Probability that a sample mean falls in the 140-150 range
prob_between = (stats.norm.cdf(150, population_mean, standard_error) - stats.norm.cdf(140, population_mean, standard_error)) * 100
print(f"P(140 ≤ sample mean ≤ 150 bpm): {prob_between:.2f}%")

# ============================================================================
# SECTION 7: Z-SCORE ANALYSIS
# ============================================================================
# Z-scores standardize values to compare them against the normal distribution
# Formula: Z = (X - mean) / standard_error
print("\n" + "="*60)
print("Z-SCORE ANALYSIS")
print("="*60)
z_140 = (140 - population_mean) / standard_error
z_150 = (150 - population_mean) / standard_error
print(f"Z-score for 140 bpm: {z_140:.4f}")
print(f"Z-score for 150 bpm: {z_150:.4f}")
print("(Interpretation: How many standard errors away from the mean)")

# ============================================================================
# SECTION 8: ADDITIONAL VISUALIZATIONS
# ============================================================================
# Create comprehensive multi-panel visualization for detailed analysis
print("\n" + "="*60)
print("GENERATING ADVANCED VISUALIZATIONS")
print("="*60)

# Create figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Subplot 1: Box plot for identifying outliers and quartiles
ax1 = axes[0, 0]
ax1.boxplot(song_tempos)
ax1.set_ylabel('Tempo (bpm)')
ax1.set_title('Box Plot - Outlier Detection')
ax1.grid(axis='y', alpha=0.3)

# Subplot 2: Histogram with fitted normal distribution curve
# Shows if data is normally distributed and identifies any skewness
ax2 = axes[0, 1]
n, bins, patches = ax2.hist(song_tempos, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
xmin, xmax = ax2.get_xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, population_mean, population_std)  # Theoretical normal distribution
ax2.plot(x, p, 'r-', linewidth=2, label='Normal Distribution')
ax2.axvline(population_mean, color='g', linestyle='--', linewidth=2, label=f'Mean = {population_mean:.2f}')
ax2.axvline(population_median, color='orange', linestyle='--', linewidth=2, label=f'Median = {population_median:.2f}')
ax2.set_xlabel('Tempo (bpm)')
ax2.set_ylabel('Density')
ax2.set_title('Histogram with Normal Distribution Overlay')
ax2.legend()
ax2.grid(alpha=0.3)

# Subplot 3: Q-Q Plot for normality assessment
# Points on the diagonal indicate data follows normal distribution
ax3 = axes[1, 0]
stats.probplot(song_tempos, dist="norm", plot=ax3)
ax3.set_title('Q-Q Plot (Normality Assessment)')
ax3.grid(alpha=0.3)

# Subplot 4: Violin plot showing distribution shape and quartiles
ax4 = axes[1, 1]
ax4.violinplot(song_tempos, vert=True)
ax4.axhline(population_mean, color='r', linestyle='--', linewidth=2, label=f'Mean = {population_mean:.2f}')
ax4.axhline(population_median, color='orange', linestyle='--', linewidth=2, label=f'Median = {population_median:.2f}')
ax4.axhline(q1, color='gray', linestyle=':', alpha=0.5, label=f'Q1 = {q1:.2f}')
ax4.axhline(q3, color='gray', linestyle=':', alpha=0.5, label=f'Q3 = {q3:.2f}')
ax4.set_ylabel('Tempo (bpm)')
ax4.set_title('Violin Plot - Distribution Shape')
ax4.legend()
ax4.grid(alpha=0.3)

plt.tight_layout()

# Save the comprehensive analysis figure to the figures directory
fig_path = os.path.join(figures_dir, '03_comprehensive_analysis.png')
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print(f"Saved: {fig_path}")
plt.show()

print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
print("All statistics calculated and visualizations generated successfully.")
print(f"\nAll figures saved to: {figures_dir}/")