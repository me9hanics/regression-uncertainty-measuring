"""
Unit and statistical tests for the functions in riskmeasures.simulation
"""
import numpy as np
from riskmeasures.simulation import simulate_data

def test_simulate_data_shape():
    data = simulate_data(10, seed=17)
    assert isinstance(data, np.ndarray)
    assert data.shape == (10, 2)

def test_simulate_data_reproducible_seed():
    d1 = simulate_data(100, seed=17)
    d2 = simulate_data(100, seed=17)
    assert np.array_equal(d1, d2)

def test_simulate_data_stats_large_n():
    """
    Statistical sanity check:
    For large N, x should be ~ N(0, x_sigma^2),
    and eps variance should be ~ epsilon_sigma^2.
    Also, y stats should match theory.
    """
    N = 200000
    beta0 = 1.0
    beta1 = 2.0
    x_sigma = 1.0
    eps_sigma = 1.0  #test a non-1 sigma too
    seed = 17

    data = simulate_data(
        N, beta_0=beta0, beta_1=beta1,
        x_sigma=x_sigma, epsilon_sigma=eps_sigma,
        seed=seed
    )
    x = data[:, 0]
    y = data[:, 1]
    eps = y - (beta0 + beta1 * x)

    assert abs(np.mean(x) - 0.0) < 0.05
    assert abs(np.mean(eps) - 0.0) < 0.05

    assert abs((np.var(x)/x_sigma**2)-1) < 0.05 #+-5%
    assert abs((np.var(eps)/eps_sigma**2)-1) < 0.05 #+-5%

    expected_mean_y = beta0
    expected_var_y = beta0**2 + beta1**2*1 + 1 - expected_mean_y**2 #see formula, in this case 5
    assert abs(np.mean(y) - expected_mean_y) < 0.05 #5%
    assert abs(np.var(y) - expected_var_y) < 0.25 #5%