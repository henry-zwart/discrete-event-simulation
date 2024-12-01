FIGURES_DIR = results/figures
DATA_DIR = data

FIGURE_NAMES = \
	exercise_2_boxplot.png \
	exercise_2_confidence_plot.png \
	wait_time_vs_measure_time.png \
	exercise_3_boxplot.png \
	exercise_4.png

FIGURES = $(patsubst %, results/figures/%, $(FIGURE_NAMES))

RHO_EX2 = 8 9 98
N_EX2 = 1 2 4
EX2_PARAMS := $(foreach rho,$(RHO_EX2),$(foreach n,$(N_EX2), $(rho)_$(n)))
EX2_MEAN_FILES = $(foreach params,$(EX2_PARAMS),data/ex2_means_$(params).npy)


# Just use the means file as the target. Require means file for each EX2_RUNS variable.
# Use this to parallelise

ENTRYPOINT ?= uv run

all: $(FIGURES)

$(FIGURES) ?: .make-figures .ex2-figures

.make-figures: \
		scripts/plot_exercise_2.py \
		scripts/exercise_4_plot.py \
		scripts/exercise_3.py \
		scripts/exercise_4.py \
		data/.ex2_data \
		| $(FIGURES_DIR)
	$(ENTRYPOINT) scripts/plot_exercise_2.py && \
	$(ENTRYPOINT) scripts/exercise_4_plot.py && \
	$(ENTRYPOINT) scripts/exercise_3.py && \
	$(ENTRYPOINT) scripts/exercise_4.py && \
	touch $@

.ex2-figures: scripts/plot_exercise_2_5.py $(EX2_MEAN_FILES)
	$(ENTRYPOINT) $< "$(RHO_EX2)" "$(N_EX2)"&& \
	touch $@

data/ex2_means_%.npy: scripts/exercise_2_5.py | $(DATA_DIR)
	$(ENTRYPOINT) $< $(subst _, ,$*)

data/.ex2_data: scripts/exercise_2.py | $(DATA_DIR)
	$(ENTRYPOINT) $< && \
	touch $@

$(FIGURES_DIR):
	mkdir -p $@

$(DATA_DIR):
	mkdir -p $@

.PHONY: clean
clean:
	rm -rf results data
