FIGURES_DIR = results/figures
DATA_DIR = data

FIGURE_NAMES = 

FIGURES = $(patsubst %, results/figures/%, $(FIGURE_NAMES))

ENTRYPOINT ?= uv run

all: 

$(FIGURES_DIR):
	mkdir -p $@

$(DATA_DIR):
	mkdir -p $@

.PHONY: clean
clean:
	rm -rf results data
