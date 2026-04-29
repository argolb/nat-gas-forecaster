# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  transform/Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean export

all: output/data_clean.parquet

clean:
	rm output/*

export: all
	@echo "Exported to output/data_clean.parquet"

output/data_clean.parquet: \
		src/transform.py \
		../import/output/data_raw.parquet
	mkdir -p output
	$(HERE)/.venv/bin/python src/transform.py \
		--input=../import/output/data_raw.parquet \
		--output=$@

# done