# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# export/src/export.py

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
	parser.add_argument("--input", default="../forecast/output/forecasts.parquet")
	parser.add_argument("--output", default="output/predictions.csv")
	args = parser.parse_args()
	return args
#}}}

# main {{{
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
	args = get_args()
	initial_asserts(args)

	logging.info(f"Loading forecasts from {args.input}")
	df = pd.read_parquet(args.input)

	logging.info(f"Writing to CSV: {args.output}")
	output_path = Path(args.output)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	df.to_csv(output_path, index=True)

	logging.info(f"Export complete: {len(df)} predictions")
#}}}
# done.