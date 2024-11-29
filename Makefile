FIGURES_DIR = results/figures
DATA_DIR = data

FIGURE_NAMES = \
	exercise_2_boxplot.png \
	exercise_2_confidence_plot.png \
	wait_time_vs_measure_time.png \
	exercise_3_boxplot.png \
	exercise_4_boxplot.png

FIGURES = $(patsubst %, results/figures/%, $(FIGURE_NAMES))

ENTRYPOINT ?= uv run

all: $(FIGURES)

$(FIGURES) ?: .make-figures

.make-figures: \
		scripts/plot_exercise_2.py \
		scripts/plot_exercise_2_5.py \
		scripts/exercise_3.py \
		scripts/exercise_4.py \
		data/.ex2_data \
		| $(FIGURES_DIR)
	$(ENTRYPOINT) scripts/plot_exercise_2.py && \
	$(ENTRYPOINT) scripts/plot_exercise_2_5.py && \
	$(ENTRYPOINT) scripts/exercise_3.py && \
	$(ENTRYPOINT) scripts/exercise_4.py && \
	touch $@

data/.ex2_data: scripts/exercise_2.py scripts/exercise_2_5.py | $(DATA_DIR)
	$(ENTRYPOINT) $< && \
	$(ENTRYPOINT) scripts/exercise_2_5.py 0.8 && \
	$(ENTRYPOINT) scripts/exercise_2_5.py 0.9 && \
	$(ENTRYPOINT) scripts/exercise_2_5.py 0.98 && \
	touch $@

$(FIGURES_DIR):
	mkdir -p $@

$(DATA_DIR):
	mkdir -p $@

.PHONY: clean
clean:
	rm -rf results data
