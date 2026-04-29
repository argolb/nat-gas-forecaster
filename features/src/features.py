# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# features/src/features.py

# ---- dependencies {{{
from pathlib import Path
import argparse
import logging
import pandas as pd
#}}}

# ---- support methods {{{
def initial_asserts(args):
	assert Path(args.input).exists()
	return 1


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", default="../transform/output/data_clean.parquet")
	parser.add_argument("--output", default="output/data_features.parquet")
	parser.add_argument("--price-col", default="Prices")
	parser.add_argument("--lags", default="1,3,6,12")
	args = parser.parse_args()
	return args


def create_features(df, price_col, lags):
	df = df.copy()
	lag_list = [int(x) for x in lags.split(',')]

	logging.info(f"Creating lag features: {lag_list}")
	for lag in lag_list:
		df[f'lag_{lag}'] = df[price_col].shift(lag)

	logging.info("Creating rolling mean (3-month)")
	df['rolling_mean_3'] = df[price_col].rolling(window=3).mean()

	logging.info("Creating rolling std (3-month)")
	df['rolling_std_3'] = df[price_col].rolling(window=3).std()

	df = df.dropna()
	logging.info(f"Feature engineering complete. Rows: {len(df)}")
	return df
#}}}

# main {{{
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
	args = get_args()
	initial_asserts(args)

	logging.info(f"Loading data from {args.input}")
	df = pd.read_parquet(args.input)

	logging.info("Adding feature columns")
	df = create_features(df, args.price_col, args.lags)

	output_path = Path(args.output)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	df.to_parquet(output_path)
	logging.info(f"Written to {output_path}")
#}}}
# done.