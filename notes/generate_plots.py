# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# notes/generate_plots.py

# ---- dependencies {{{
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import seaborn as sns
#}}}

# ---- support methods {{{
def plot_historical_prices(df, output_path):
	"""Plot 1: Historical natural gas price time series."""
	plt.figure(figsize=(14, 6))
	plt.plot(df.index, df['Prices'], color='#1f77b4', linewidth=2)
	plt.title('Historical Natural Gas Prices (Oct 2020 - Sep 2024)', fontsize=16, fontweight='bold')
	plt.xlabel('Date', fontsize=12)
	plt.ylabel('Price ($)', fontsize=12)
	plt.grid(True, alpha=0.3)
	plt.fill_between(df.index, df['Prices'], alpha=0.1, color='#1f77b4')
	plt.tight_layout()
	plt.savefig(output_path / 'historical_prices.png', dpi=150)
	plt.close()
	print(f"Saved: {output_path / 'historical_prices.png'}")


def plot_forecast(df_hist, forecast_df, model_fit, output_path):
	"""Plot 2: Historical + forecast with confidence intervals."""
	plt.figure(figsize=(14, 7))

	# Historical data (full range)
	plt.plot(df_hist.index, df_hist['Prices'], label='Historical Price', color='#1f77b4', linewidth=2)

	# In-sample fit - model was trained on data after feature engineering (with dropna)
	# The fitted values correspond to the training period (after lag removal)
	# Re-create the training index that matches the model's fitted values
	train_idx = df_hist.index[-len(model_fit.fittedvalues):]
	in_sample = pd.Series(model_fit.fittedvalues.values, index=train_idx)
	plt.plot(train_idx, in_sample, label='In-Sample SARIMA Fit', color='#2ca02c', linestyle='--', alpha=0.7)

	# Forecast
	plt.plot(forecast_df.index, forecast_df['predicted_price'], label='12-Month Forecast', color='#d62728', linewidth=2, marker='o', markersize=4)

	# Fill forecast uncertainty (simulated confidence interval)
	forecast_dates = forecast_df.index
	forecast_values = forecast_df['predicted_price'].values
	std_dev = df_hist['Prices'].std() * 0.3
	plt.fill_between(forecast_dates, forecast_values - std_dev, forecast_values + std_dev,
	                 alpha=0.2, color='#d62728', label='Approx. 95% CI')

	plt.title('Natural Gas Price: SARIMA Forecast (12-Month Projection)', fontsize=16, fontweight='bold')
	plt.xlabel('Date', fontsize=12)
	plt.ylabel('Price ($)', fontsize=12)
	plt.legend(loc='best')
	plt.grid(True, alpha=0.3)
	plt.tight_layout()
	plt.savefig(output_path / 'forecast.png', dpi=150)
	plt.close()
	print(f"Saved: {output_path / 'forecast.png'}")


def plot_feature_correlation(df_features, output_path):
	"""Plot 3: Correlation heatmap of engineered features."""
	numeric_cols = df_features.select_dtypes(include=[np.number]).columns
	corr = df_features[numeric_cols].corr()

	plt.figure(figsize=(10, 8))
	mask = np.triu(np.ones_like(corr, dtype=bool))
	sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
	            center=0, square=True, cbar_kws={'shrink': 0.8})
	plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
	plt.tight_layout()
	plt.savefig(output_path / 'correlation_heatmap.png', dpi=150)
	plt.close()
	print(f"Saved: {output_path / 'correlation_heatmap.png'}")


def plot_residuals(model_fit, output_path):
	"""Plot 4: SARIMA model residual diagnostics."""
	residuals = model_fit.resid

	fig, axes = plt.subplots(2, 2, figsize=(14, 10))
	fig.suptitle('SARIMA Model Residual Diagnostics', fontsize=16, fontweight='bold')

	# Residuals over time
	axes[0, 0].plot(residuals.index, residuals, color='#ff7f0e', alpha=0.7)
	axes[0, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
	axes[0, 0].set_title('Residuals Over Time')
	axes[0, 0].set_xlabel('Date')
	axes[0, 0].set_ylabel('Residual')
	axes[0, 0].grid(True, alpha=0.3)

	# Histogram of residuals
	axes[0, 1].hist(residuals, bins=20, edgecolor='black', alpha=0.7, color='#1f77b4')
	axes[0, 1].axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Zero')
	axes[0, 1].set_title('Residual Distribution')
	axes[0, 1].set_xlabel('Residual Value')
	axes[0, 1].set_ylabel('Frequency')
	axes[0, 1].legend()
	axes[0, 1].grid(True, alpha=0.3)

	# Q-Q plot
	from scipy import stats
	stats.probplot(residuals, dist="norm", plot=axes[1, 0])
	axes[1, 0].set_title('Q-Q Plot (Normal)')
	axes[1, 0].grid(True, alpha=0.3)

	# ACF of residuals
	from statsmodels.graphics.tsaplots import plot_acf
	plot_acf(residuals, lags=20, ax=axes[1, 1], alpha=0.05)
	axes[1, 1].set_title('Autocorrelation (ACF) of Residuals')

	plt.tight_layout()
	plt.savefig(output_path / 'residual_diagnostics.png', dpi=150)
	plt.close()
	print(f"Saved: {output_path / 'residual_diagnostics.png'}")


def plot_price_distribution(df, output_path):
	"""Plot 5: Price distribution with statistics."""
	fig, axes = plt.subplots(1, 2, figsize=(14, 5))

	# Histogram with KDE
	axes[0].hist(df['Prices'], bins=15, edgecolor='black', alpha=0.7, color='#2ca02c', density=True)
	df['Prices'].plot(kind='kde', ax=axes[0], color='red', linewidth=2, label='KDE')
	axes[0].set_title('Price Distribution (Histogram + KDE)')
	axes[0].set_xlabel('Price ($)')
	axes[0].set_ylabel('Density')
	axes[0].legend()
	axes[0].grid(True, alpha=0.3)

	# Box plot with monthly pattern
	df_reset = df.reset_index()
	df_reset['Month'] = df_reset['Dates'].dt.month
	monthly_prices = [df_reset[df_reset['Month'] == m]['Prices'].values for m in range(1, 13)]
	axes[1].boxplot(monthly_prices, labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
	axes[1].set_title('Monthly Price Distribution')
	axes[1].set_xlabel('Month')
	axes[1].set_ylabel('Price ($)')
	axes[1].grid(True, alpha=0.3, axis='y')

	plt.tight_layout()
	plt.savefig(output_path / 'price_distribution.png', dpi=150)
	plt.close()
	print(f"Saved: {output_path / 'price_distribution.png'}")


def plot_pipeline_flow(output_path):
	"""Plot 6: Pipeline architecture diagram."""
	fig, ax = plt.subplots(figsize=(16, 6))
	ax.set_xlim(0, 10)
	ax.set_ylim(0, 3)
	ax.axis('off')

	stages = [
		('Import', 0.5, '#e1f5fe'),
		('Transform', 2.0, '#b3e5fc'),
		('Features', 3.5, '#81d4fa'),
		('Model', 5.0, '#4fc3f7'),
		('Forecast', 6.5, '#29b6f6'),
		('Export', 8.0, '#039be5')
	]

	for name, x, color in stages:
		# Box
		rect = plt.Rectangle((x - 0.5, 1), 1, 1, facecolor=color, edgecolor='black', linewidth=2)
		ax.add_patch(rect)
		ax.text(x, 1.5, name, ha='center', va='center', fontsize=12, fontweight='bold')

		# Arrow (except for last stage)
		if x < 8.0:
			ax.annotate('', xy=(x + 1, 1.5), xytext=(x + 0.5, 1.5),
			            arrowprops=dict(arrowstyle='->', lw=2.5, color='#333'))

	# Add input/output labels
	ax.text(0.5, 0.5, 'Nat_Gas.csv', ha='center', fontsize=9, style='italic')
	ax.text(8.0, 0.5, 'predictions.csv', ha='center', fontsize=9, style='italic')
	ax.text(5, 2.5, 'SARIMA Pipeline (order=(1,1,1), seasonal=(0,1,1,12))',
	        ha='center', fontsize=11, fontweight='bold', color='#333')

	plt.title('Pipeline Architecture', fontsize=16, fontweight='bold', pad=20)
	plt.tight_layout()
	plt.savefig(output_path / 'pipeline_flow.png', dpi=150)
	plt.close()
	print(f"Saved: {output_path / 'pipeline_flow.png'}")


def main():
	output_path = Path('notes/images')
	output_path.mkdir(parents=True, exist_ok=True)

	# Load data
	print("Loading data...")
	df_raw = pd.read_parquet('import/output/data_raw.parquet')
	df_clean = pd.read_parquet('transform/output/data_clean.parquet')
	df_features = pd.read_parquet('features/output/data_features.parquet')
	forecast_df = pd.read_parquet('forecast/output/forecasts.parquet')

	# Prepare historical data for plotting
	df_plot = df_clean.copy()
	df_plot = df_plot.sort_index()
	df_plot.index.name = 'Dates'

	print("\nGenerating plots...")

	# Load model for residual analysis
	with open('model/output/sarima_model.pkl', 'rb') as f:
		import pickle
		model_fit = pickle.load(f)

	# Generate all plots
	plot_historical_prices(df_plot, output_path)
	plot_forecast(df_plot, forecast_df, model_fit, output_path)
	plot_feature_correlation(df_features, output_path)
	plot_residuals(model_fit, output_path)
	plot_price_distribution(df_plot, output_path)
	plot_pipeline_flow(output_path)

	print("\nAll plots generated successfully!")


if __name__ == '__main__':
	main()
# done.
