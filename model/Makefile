# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  model/Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean export

all: output/sarima_model.pkl

clean:
	rm output/*

export: all
	@echo "Exported to output/sarima_model.pkl"

output/sarima_model.pkl: \
		src/model.py \
		../features/output/data_features.parquet
	mkdir -p output
	$(HERE)/.venv/bin/python src/model.py \
		--input=../features/output/data_features.parquet \
		--output=$@

# done