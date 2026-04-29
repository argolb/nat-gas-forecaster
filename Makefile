# -*- coding: utf-8 -*-
#  :vim ft=make:
# Author: LB
# Maintainer(s): LB
#  Makefile
# -----------------------------------------------------------

HERE := $(shell git rev-parse --show-toplevel)

.PHONY: all clean train predict import transform features model forecast export

all:
	@echo "Running import..."
	@$(MAKE) -C import
	@echo "Running transform..."
	@$(MAKE) -C transform
	@echo "Running features..."
	@$(MAKE) -C features
	@echo "Running model..."
	@$(MAKE) -C model
	@echo "Running forecast..."
	@$(MAKE) -C forecast
	@echo "Running export..."
	@$(MAKE) -C export

clean:
	rm -rf import/output/* transform/output/* features/output/* model/output/* forecast/output/* export/output/*

train: import transform features model

predict: forecast export

import:
	$(MAKE) -C import

transform: import
	$(MAKE) -C transform

features: transform
	$(MAKE) -C features

model: features
	$(MAKE) -C model

forecast: model
	$(MAKE) -C forecast

export: forecast
	$(MAKE) -C export

# done