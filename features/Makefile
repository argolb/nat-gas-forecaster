# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  features/Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean export

all: output/data_features.parquet

clean:
	rm output/*

export: all
	@echo "Exported to output/data_features.parquet"

output/data_features.parquet: \
		src/features.py \
		../transform/output/data_clean.parquet
	mkdir -p output
	$(HERE)/.venv/bin/python src/features.py \
		--input=../transform/output/data_clean.parquet \
		--output=$@

# done