# Presentation

## Overview
Implemented:
- Functions (Task 1-3) in both Python and R
- Input sanity checks
- Packaging as Python library
- Tests in Python
- Parallelization in Python (and vectorization)
- CLI to run end-to-end from command line
- Storing results with metadata in JSON, CSV
- GitHub Actions for CI

## Simulate data

**Python:**

![Python simulation code](images/simulate-data-code.png)

**R:**

![R simulation code](images/simulate-data-code-R.png)

- Instead of just sigma, had `sigma_x` and `sigma_epsilon` for generality
- RNG seed for reproducibility (saved with results)
- Data stored in numpy arrays but validation accepts array-like (lists, pd.Series, etc.)

---

## Simulated data distribution

![Data distribution plot](images/simulated-data-distribution-plot.png)

- Means and variances are correct
- Data saved into CSV in artifacts folder

---

## Simulation variance formula

![Variance formula](images/simulation-variance-formula.png)

---

## Estimate beta

Simple approach:

**Python:**

![Python beta estimation](images/estimate-beta-code.png)

**R:**

![R beta estimation](images/estimate-beta-code-R.png)

---

## Estimate beta - alternative approach

![Alternative beta estimation](images/estimate-beta-code-2.png)

- Tried `np.linalg.lstsq()` too
- Results: not actually faster (tried until I ran out of memory), and produced same results numerically
- This is just due to 2×2 matrix inversion being very fast - for higher dimensions it is worth using `lstsq()`

---

## Bootstrap sampling

**Python:**

![Python bootstrap samples](images/bootstrap-samples-code.png)

**R:**

![R bootstrap samples](images/bootstrap-samples-code-R.png)

- Vectorized implementation
- Memory tradeoff

---

## Standard deviation

**Python:**

![Python standard deviation code](images/sample-std-code.png)

**R:**

![R standard deviation code](images/sample-std-code-R.png)

---

## Beta standard error from bootstrap

**Python:**

![Python bootstrap beta](images/bootstrap-beta-code.png)

**R:**

![R bootstrap beta](images/bootstrap-beta-code-R.png)

---

## Parallelization

Four options considered:

- **Multithreading**
- **Multiprocessing**
- **Distributed computing**
- **Hardware acceleration** (via vectorization)

---

## Parallelization - implementation

Using **Joblib** for multiprocessing and multithreading:

![Parallel bootstrap code](images/bootstrap-beta-code-parallel.png)

---

## Parallelization - results

- Didn't speed up for this case
- Reason: `estimate_beta()` calls are still very fast (2×2 matrix inversion), so the overhead of parallelization is not worth it here
- On more sophisticated (8D) data, it tested to be faster

---

## Input sanity checks

**R:**

![R sanity checks](images/sanity-check-funcs-R.png)

**Python:**

![Python sanity checks 1](images/sanity-check-funcs.png)
![Python sanity checks 2](images/sanity-check-funcs-2.png)

Standard checks in Python - functions for range, type, shape written in `utils.py` and called at function entrypoints.

---

## Tests

![Simulation tests](images/tests-simulation-code.png)
![Methods tests](images/tests-methods-code.png)

- **Pytest** (GitHub Actions automated)
- Model sanity: across many Monte Carlo repetitions, similar value for `beta_hat` (converges to `beta_true`)

---

## Choosing B value

![Relative error formula](images/relative-error-formula.png)

**Option A:** 5% relative error (to original variance) at around B=200

**Option B:** "Parameter-tuning for B" - increase B gradually, cut off SE after less than 1% diff between one measurement and k-100th measurement

---

## CLI and data storage

![CLI example](images/cli.png)

- Command-line interface implemented
- Tried for R too with AI help, has bugs though

---

## GitHub actions

![GitHub workflow](images/github-workflow-code.png)

Automated testing on push.

---

## Others

- Docstrings
- Type hints
- Packaging as module
- README documentation


### For future:

- **Linting** (with ruff): Auto checks code for bugs, PEP8 style guide violations, complexity
- **Formatting**: Auto formats code (ruff, black)
- **Documentation**: Auto-generation possible with Sphinx, pdoc or pydocstyle
- Could use `**kwargs` to simplify, or at least params dict: `{'N': N, 'sigma': sigma, ...}`