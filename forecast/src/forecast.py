# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# forecast/src/forecast.py

# ---- dependencies {{{
from pathlib import Path
import argparse
import logging
import pickle
import pandas as pd
#}}}

# ---- support methods {{{
def initial_asserts(args):
	assert Path(args.model).exists()
	return 1


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--model", default="../model/output/sarima_model.pkl")
	parser.add_argument("--input", default="../transform/output/data_clean.parquet")
	parser.add_argument("--output", default="output/forecasts.parquet")
	parser.add_argument("--horizon", default="12")
	args = parser.parse_args()
	return args
#}}}

# main {{{
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
	args = get_args()
	initial_asserts(args)

	logging.info(f"Loading model from {args.model}")
	with open(args.model, 'rb') as f:
		model_fit = pickle.load(f)

	logging.info(f"Loading historical data from {args.input}")
	df = pd.read_parquet(args.input)

	last_date = df.index[-1]
	forecast_end = last_date + pd.DateOffset(months=int(args.horizon))

	logging.info(f"Generating {args.horizon}-month forecast from {last_date} to {forecast_end}")

	future_dates = pd.date_range(start=last_date, periods=int(args.horizon) + 1, freq='ME')[1:]

	forecasts = model_fit.forecast(steps=int(args.horizon))
	forecasts.index = future_dates

	result = pd.DataFrame({
		'date': forecasts.index,
		'predicted_price': forecasts.values
	})
	result = result.set_index('date')

	output_path = Path(args.output)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	result.to_parquet(output_path)

	logging.info(f"Written forecasts to {output_path}")
	logging.info(f"Forecast range: {result.index.min()} to {result.index.max()}")
#}}}
# done.