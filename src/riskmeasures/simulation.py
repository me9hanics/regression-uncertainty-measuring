import numpy as np
from riskmeasures.utils import validate_int, validate_positive

def simulate_data(N : int,
                  beta_0 : float = 1,
                  beta_1 : float = 2,
                  x_sigma : float = 1,
                  epsilon_sigma : float = 1,
                  seed : int | None = None
                  ) -> np.ndarray:
    """
    Simulate data according to the linear regression model:
        y_i = beta_0 + beta_1 * x_i + epsilon_i,  i = 1, ..., N

    where:
        x_i ~ N(0, x_sigma^2)
        epsilon_i ~ N(0, epsilon_sigma^2)
    
    Returns a 2D array where each row is an (x, y) pair.

    Parameters
    ----------
    N : int
        Number of observations to generate.
    beta_0 : float
        Intercept of the regression model.
    beta_1 : float
        Slope of the regression model.
    x_sigma : float
        Standard deviation of the x values.
    epsilon_sigma : float
        Standard deviation of the error terms.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    data : np.ndarray
        A 2D array where each row is an (x, y) pair.
    """
    validate_int("N", N, min_value=2)
    validate_positive("x_sigma", x_sigma)
    validate_positive("epsilon_sigma", epsilon_sigma)

    rng = np.random.default_rng(seed)
    xs = rng.normal(0, x_sigma, N)
    epsilons = rng.normal(0, epsilon_sigma, N)
    ys = beta_0 + beta_1 * xs + epsilons
    data = np.column_stack((xs, ys))
    return data
