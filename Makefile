FIGURES_DIR = results/figures
DATA_DIR = data

FIGURE_NAMES = \
	exercise_2_boxplot.png \
	exercise_2_confidence_plot.png \
	wait_time_vs_measure_time.png \
	exp_wait_at_5000.png \
	exercise_3_boxplot.png \
	exercise_4.png

FIGURES = $(patsubst %, results/figures/%, $(FIGURE_NAMES))

RHO_EX2 = 8 9 98
N_EX2 = 1 2 4
EX2_PARAMS := $(foreach rho,$(RHO_EX2),$(foreach n,$(N_EX2), $(rho)_$(n)))
EX2_MEAN_FILES = $(foreach params,$(EX2_PARAMS),data/ex2_means_$(params)_5000_fifo.npy) \
	$(foreach rho,$(RHO_EX2),data/ex2_means_$(rho)_1_5000_prio.npy)

ENTRYPOINT ?= uv run

all: $(FIGURES)

$(FIGURES) ?: .make-figures .ex2-figures

.make-figures: \
		scripts/plot_exercise_2.py \
		scripts/exercise_4_plot.py \
		data/.ex4_data \
		data/.ex2_data \
		| $(FIGURES_DIR)
	$(ENTRYPOINT) scripts/plot_exercise_2.py && \
	$(ENTRYPOINT) scripts/exercise_4_plot.py && \
	touch $@

.ex2-figures: scripts/plot_exercise_2_5.py $(EX2_MEAN_FILES)
	$(ENTRYPOINT) $< "$(RHO_EX2)" "$(N_EX2)"&& \
	touch $@

data/ex2_means_%_5000_fifo.npy: scripts/exercise_2_5.py | $(DATA_DIR)
	$(ENTRYPOINT) $< $(subst _, ,$*)

data/ex2_means_%_1_5000_prio.npy: scripts/exercise_3.py | $(DATA_DIR)
	$(ENTRYPOINT) $< $*

data/.ex4_data: scripts/exercise_4.py | $(DATA_DIR)
	$(ENTRYPOINT) $< && \
	touch $@

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
