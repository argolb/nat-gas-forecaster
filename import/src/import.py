# vim: set ts=4 sts=0 sw=4 si fenc=utf-8 et:
# vim: set fdm=marker fmr={{{,}}} fdl=0 foldcolumn=4:
# Authors:     LB
# Maintainers: LB
# Copyright:   2026,  GPL v2 or later
# =========================================
# import/src/import.py

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
	parser.add_argument("--input", default="import/input/Nat_Gas.csv")
	parser.add_argument("--output", default="import/output/data_raw.parquet")
	args = parser.parse_args()
	return args
#}}}

# main {{{
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
	args = get_args()
	initial_asserts(args)

	input_path = Path(args.input)
	logging.info(f"Loading data from {input_path}")

	df = pd.read_csv(input_path)
	logging.info(f"Loaded {len(df)} rows")

	output_path = Path(args.output)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	df.to_parquet(output_path)
	logging.info(f"Written to {output_path}")
#}}}
# done.