# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# model/src/model.py

# ---- dependencies {{{
from pathlib import Path
import argparse
import logging
import pickle
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
#}}}

# ---- support methods {{{
SARIMA_ORDER = (1, 1, 1)
SARIMA_SEASONAL_ORDER = (0, 1, 1, 12)


def initial_asserts(args):
	assert Path(args.input).exists()
	return 1


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", default="../features/output/data_features.parquet")
	parser.add_argument("--output", default="output/sarima_model.pkl")
	parser.add_argument("--price-col", default="Prices")
	args = parser.parse_args()
	return args
#}}}

# main {{{
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
	args = get_args()
	initial_asserts(args)

	logging.info(f"Loading data from {args.input}")
	df = pd.read_parquet(args.input)

	prices = df[args.price_col]
	logging.info(f"Training SARIMA model: order={SARIMA_ORDER}, seasonal={SARIMA_SEASONAL_ORDER}")

	model = SARIMAX(
		prices,
		order=SARIMA_ORDER,
		seasonal_order=SARIMA_SEASONAL_ORDER,
		enforce_stationarity=False,
		enforce_invertibility=False
	)
	model_fit = model.fit(disp=False)

	output_path = Path(args.output)
	output_path.parent.mkdir(parents=True, exist_ok=True)

	with open(output_path, 'wb') as f:
		pickle.dump(model_fit, f)

	logging.info(f"Model saved to {output_path}")
#}}}
# done.