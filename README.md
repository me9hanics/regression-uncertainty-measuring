# Assignment repository - regression uncertainty calculation in R and Python

This repo stores the codes for the solutions to the tasks AND other tools for future usecases. It implements a linear model data generation function and measures, as a Python package. The repository design resembles a practical package design with codebase, CLI, "logging", tests, data artifacts and CI/CD.

While most of the focus is on the Python implementation, the specific tasks were also implemented in R (as convenience for the team). The below instructions focus on the Python package usage though.

---

## How to replicate - install etc. (Import lib)

1. Download the repository
2. Open its root path in a terminal
3. Create a virtual environment using the `pyproject.toml` file, I recommend using `uv`:
   ```bash
   uv venv
   ```
4. Activate the venv:
   - **Windows:** `.venv\Scripts\activate`
   - **Linux/Mac:** `source .venv/bin/activate`
5. Install the package in editable mode:
   ```bash
   uv pip install -e .
   ```

---

## Example usage - Quick start, CLI

You can run the full pipeline from the command line interface (CLI). An example command is:

```bash
python -m riskmeasures.cli --N 10000 --B 1000 --x-sigma 1.0 --eps-sigma 1.0 --seed 17 --log
```

then check the `artifacts/` folder for outputs.
---

## Parallelization

For the pipeline using `--parallel --n-jobs 6`, and in `bootstrap_beta`, multiprocesssing can be used.

---

## Seeds

To ensure reproducibility, you can use random seeds with `--seed`, similarly for most functions.

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

