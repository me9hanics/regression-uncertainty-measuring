# Assignment repository - regression uncertainty calculation in R and Python

This repo stores the codes for the solutions to the tasks AND other tools for future usecases. It implements a linear model data generation function and measures, as a Python package. The repository design resembles a practical package design with codebase, CLI, "logging", tests, data artifacts and CI/CD.

While most of the focus is on the Python implementation, the specific tasks were also implemented in R (as convenience for the team). The below instructions focus on the Python package usage though.

The solutions were first developed in Python, and then "recreated" in R.<br>
Python code can be found in `src/riskmeasures/`, R code in `src/riskmeasures-R/`.

---

## How to: replicate, install etc.

### R
1. Download the repository
2. Open its root path in RStudio as a new project
Optional: for the *experimental* CLI running,

### Python
1. Download the repository
2. Open its root path in a terminal
3. Create a virtual environment from the `pyproject.toml` file, I recommend using `uv`:
   ```bash
   uv venv
   ```
   (`uv` automatically detects the `pyproject.toml` file.)
4. Activate the venv:
   - **Windows:** `.venv\Scripts\activate`
   - **Linux/Mac:** `source .venv/bin/activate`
5. Install the package (optionally in editable mode):
   ```bash
   uv pip install -e .
   ```

---

## Quick start, Example usage with CLI

You can run the full pipeline simply from the command line. Just open it and run e.g.:

```bash
python -m riskmeasures.cli --N 10000 --B 1000 --x-sigma 1.0 --eps-sigma 1.0 --seed 17 --log
```

then check the `artifacts/` folder for outputs (results, data and input parameters all stored).

<br>The R version would use the `riskmeasures-R/cli.R` script, however currently the CLI argument parsing is buggy.

---

## Parallelization

The pipeline can be parallelized, using `--parallel --n-jobs 6` (change number), these are arguments for `bootstrap_beta`. This utilizes multiprocesssing.

---

## Seeds

To ensure reproducibility, you can use fixed random seeds with `--seed`, similarly for most functions.

---

## Output artifacts

The outputs (data, results) are stored in the `artifacts/` folder by default. I store the data as a CSV, and the parameters (both input and output) as a JSON file. This makes it easy to check (audit) later, and to be exposed via an API if needed.

You can specify paths using the `--out` and `--save-data` arguments for saving the results.

---

## Running tests

In this case, rather create a dev environment:

```bash
uv pip install -e .[dev]
```

Then run tests with:

```bash
pytest
```

---

## Extras

- Type hinting ✓
- Docstrings ✓
- Presentation slides: Work In Progress

---

## Future additions

- GitHub Actions CI/CD (soon) to run tests on each push
- Add `ruff` for linting, style checking
- API design?

