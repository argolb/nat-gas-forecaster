# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  export/Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean export

all: output/predictions.csv

clean:
	rm output/*

export: all
	@echo "Exported to output/predictions.csv"

output/predictions.csv: \
		src/export.py \
		../forecast/output/forecasts.parquet
	mkdir -p output
	$(HERE)/.venv/bin/python src/export.py \
		--input=../forecast/output/forecasts.parquet \
		--output=$@

# done