import numpy as np
from riskmeasures.simulation import simulate_data
from riskmeasures.methods import estimate_beta, bootstrap_samples, bootstrap_beta

def test_estimate_beta_no_epsilon():
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    data = np.column_stack([x, y])

    beta_hat = estimate_beta(data)
    assert beta_hat.shape == (2,)
    assert np.allclose(beta_hat, np.array([1.0, 2.0]), atol=1e-12)

def test_bootstrap_samples_shape():
    data = simulate_data(20, seed=17)
    B = 50
    samples = bootstrap_samples(data, B)
    assert samples.shape == (B, 20, 2)

def test_bootstrap_beta_return():
    data = simulate_data(200, seed=17)
    se = bootstrap_beta(data, B=200, parallel=False)
    assert isinstance(se, float)
    assert se > 0.0

def test_bootstrap_beta_reproducible_seed():
    data = simulate_data(200, seed=17)

    se1 = bootstrap_beta(data, B=200, parallel=False, seed=17)
    se2 = bootstrap_beta(data, B=200, parallel=False, seed=17)

    assert abs(se1 - se2) < 1e-12
    assert se1 > 0.0 and se2 > 0.0

def test_bootstrap_se_decreases_with_n():
    data_small = simulate_data(100, seed=7)
    data_big = simulate_data(1000, seed=7)

    se_small = bootstrap_beta(data_small, B=300, parallel=False)
    se_big = bootstrap_beta(data_big, B=300, parallel=False)

    assert se_big < se_small