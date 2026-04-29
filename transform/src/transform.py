# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# transform/src/transform.py

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
	parser.add_argument("--input", default="import/output/data_raw.parquet")
	parser.add_argument("--output", default="transform/output/data_clean.parquet")
	parser.add_argument("--date-col", default="Dates")
	parser.add_argument("--price-col", default="Prices")
	parser.add_argument("--date-format", default="%m/%d/%y")
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

	logging.info(f"Parsing dates with format {args.date_format}")
	df[args.date_col] = pd.to_datetime(df[args.date_col], format=args.date_format)

	logging.info("Setting date as index")
	df = df.set_index(args.date_col)

	logging.info("Sorting and resampling to monthly end")
	df = df.sort_index().asfreq('ME')

	logging.info(f"Historical range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")

	output_path = Path(args.output)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	df.to_parquet(output_path)
	logging.info(f"Written to {output_path}")
#}}}
# done.