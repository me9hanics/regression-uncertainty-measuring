import numpy as np
from joblib import Parallel, delayed
#from numpy.random import SeedSequence
from riskmeasures.utils import validate_xy_data, validate_int, validate_rng_seed

def estimate_beta(data: np.ndarray
                  ) -> np.ndarray:
    """
    Gets the coefficients of a 2D OLS model fitted to the input, based on the formula:

    beta_hat = (X^T X)^{-1} X^T y

    where X is the design matrix (NOT THE INPUT!), and y is the response vector. 
    
    Parameters
    ----------
    data : np.ndarray
        A 2D array where each row is an (x, y) pair.
    
    Returns
    -------
    beta : np.ndarray
        A 1D array containing the OLS coefficient estimates (intercept and slope).
    """
    data = validate_xy_data(data, min_rows=2) #cannot fit a line without 2 points

    xs = data[:, 0]
    ys = data[:, 1]
    design = np.column_stack((np.ones(len(xs)), xs))
    beta = np.linalg.inv(design.T @ design) @ design.T @ ys
    return beta

def bootstrap_samples(data: np.ndarray, B: int,
                      seed: int = None) -> np.ndarray:
    """
    Returns an array of B bootstrap samples (shape: B x N x 2).
    Fast, due to vectorization, and no loops.

    Parameters
    ----------
    data : np.ndarray
        A 2D array where each row is an (x, y) pair.
    B : int
        Number of bootstrap samples to generate.
    seed : int, optional
        Random seed for reproducibility. Default is None.
        
    Returns
    -------
    samples : np.ndarray
        An array of shape (B, N, 2) containing the bootstrap samples.
    """
    data = validate_xy_data(data, min_rows=2)
    validate_int("B", B, min_value=1)
    _, rng = validate_rng_seed(seed)
    
    n = data.shape[0]
    indices = rng.integers(0, n, size=(B, n))
    samples = data[indices]
    return samples

def sample_std(values: np.ndarray) -> float:
    """
    Implements the sample standard deviation formula.
    (Numpy's std function implements the same, more generally.)

    Parameters
    ----------
    values : np.ndarray
        A 1D array of numerical values.
    
    Returns
    -------
    float
        The sample standard deviation of the input values.

    Raises
    ------
    ValueError
        If values is not 1D or has fewer than 2 elements.
    """
    values = np.asarray(values)
    if values.ndim != 1:
        raise ValueError(f"values must be a 1D array-like. Got ndim={values.ndim}")
    if len(values) < 2:
        raise ValueError(f"values must have at least 2 elements. Got len={len(values)}")
    
    n = len(values)
    mean_value = np.mean(values)
    variance = np.sum((values - mean_value) ** 2) / (n - 1)
    return np.sqrt(variance)

def bootstrap_beta(data: np.ndarray, B: int,
                   parallel: bool = False,
                   n_jobs: int = 1,
                   seed: int = None
                   ) -> float:
    """
    Estimates the standard error of the OLS slope coefficient using bootstrap resampling.
    
    Parameters
    ----------
    data : np.ndarray
        A 2D array where each row is an (x, y) pair.
    B : int
        Number of bootstrap samples to generate.
    parallel : bool, optional
        Whether to use parallel processing - default is False.
    n_jobs : int, optional
        Number of parallel jobs to run if parallel is True. Default is 1.
    seed : int, optional
        Random seed for reproducibility. Default is None.
    
    Notes
    -----
    Parallel mode may only be beneficial for large dimensional 
        
    Returns
    -------
    se_beta1_hat : float
        The estimated standard error of the slope coefficient.
    """
    data = validate_xy_data(data, min_rows=2)
    validate_int("B", B, min_value=2)
    validate_int("n_jobs", n_jobs, min_value=1)
    if not isinstance(parallel, bool):
        raise TypeError(f"parallel must be a bool, got {type(parallel).__name__}")
    seed, _ = validate_rng_seed(seed)
    
    samples = bootstrap_samples(data, B=B, seed=seed)
    if not parallel:
        betas = [estimate_beta(sample) for sample in samples]
    else:
        betas = Parallel(n_jobs=n_jobs)(
            delayed(estimate_beta)(sample) for sample in samples
        )
    betas = np.array(betas)
    se_beta1_hat = sample_std(betas[:, 1])
    return se_beta1_hat