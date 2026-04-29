# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  import/Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean export

all: output/data_raw.parquet

clean:
	rm output/*

export: all
	@echo "Exported to output/data_raw.parquet"

output/data_raw.parquet: \
		src/import.py \
		input/Nat_Gas.csv
	mkdir -p output
	$(HERE)/.venv/bin/python src/import.py \
		--input=input/Nat_Gas.csv \
		--output=$@

# done