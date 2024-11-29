FIGURES_DIR = results/figures
DATA_DIR = data

FIGURE_NAMES = exercise_2_boxplot.png exercise_2_confidence_plot.png

FIGURES = $(patsubst %, results/figures/%, $(FIGURE_NAMES))
RHO = 0.5 0.65 0.8 0.95

ENTRYPOINT ?= uv run

all: .make-figures

.make-figures: scripts/plot_exercise_2.py 
$(FIGURES_DIR):
	mkdir -p $@

$(DATA_DIR):
	mkdir -p $@

.PHONY: clean
clean:
	rm -rf results data
