
- Intro ....
- "Context" ....
Structure, etc. details

R CODE TOO!

### Intro, structure, details



### Simulate data
- Code screenshot
- Instead of just sigma, had sigma_x and sigma_epsilon for generality
- Also, rng seed for reproducibility  (which is then saved)


Notes: - I store in numpy arrays; sometimes for an API you might want to have your own class, dataclass, but I choose simplicity here

### Simulated data distribution plot
- Means, and variances correct.
- Show formula for y variance theoretically 5
- Also data saved into csv, in artifacts folder

### Estimate beta
- Simple approach (show code screenshot)
- Tried np.linalg.lstsq() too. Results: not actually faster (tried until I ran out of memory for the data), and produced same results numerically. But this is just due to 2x2 matrix inversion being very fast - higher dims it is worth it to use this function

### Bootstrap sampling
- Show vectorized code, mention memory tradeoff

### Beta standard error from bootstrap
- Show code screenshot

### Parallelization
- 4 options (show as bubbles)
    - Multithreading
    - Multiprocessing
    - Distributed computing
    - Hardware acceleration (via vectorization)

### Parallelization +1 slide
- "Cross out" the distributed computing and hardware acceleration options
- Display "Joblib" - as it can do both multiprocessing and multithreading
- Joblib didn't speed up - the reason is estimate_beta() calls are still very fast (2x2 matrix inversion), so the overhead of parallelization is not worth it here.
Tested on more sophisticated data 8D data, there it was already faster.

### Input sanity checks
- I used quite standard checks in Python - function for range, type, shape, these are written in utils.py and called at function entrypoints

### Tests

- OPTIONAL: Model sanity: across many Monte Carlo repetitions, similar value for beta_hat (converges to beta_true)

### Good B value?

- Formulas
- ??????????????????????????????????

### CLI, storing data

### GitHub Actions

### Extras:
- 