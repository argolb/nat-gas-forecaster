# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  forecast/Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean export

all: output/forecasts.parquet

clean:
	rm output/*

export: all
	@echo "Exported to output/forecasts.parquet"

output/forecasts.parquet: \
		src/forecast.py \
		../model/output/sarima_model.pkl \
		../transform/output/data_clean.parquet
	mkdir -p output
	$(HERE)/.venv/bin/python src/forecast.py \
		--model=../model/output/sarima_model.pkl \
		--input=../transform/output/data_clean.parquet \
		--output=$@

# done