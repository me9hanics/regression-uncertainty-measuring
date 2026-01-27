"""
Utility functions for input validation, data handling, other utils.
"""
from __future__ import annotations #Useful for newer Python versions - better type hinting (Optional[int])

from typing import Any, Optional
import numpy as np


def validate_int(name: str, value: Any, *,
                 min_value: Optional[int] = None,
                 max_value: Optional[int] = None) -> int:
    """
    Validate that value is an int (not bool) and in a given (optional) range.
    
    Parameters
    ----------
    name : str
        The name of the parameter (for error messages).
    value : Any
        The value to validate.
    min_value : Optional[int], optional
        Minimum allowed value (inclusive), by default None.
    max_value : Optional[int], optional
        Maximum allowed value (inclusive), by default None.
    
    Returns
    -------
    int
        The validated integer value.

    Raises
    ------
    TypeError
        If value is not an int (or is a bool).
    ValueError
        If value is outside the specified range.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}: {value!r}")
    if min_value is not None and value < min_value:
        raise ValueError(f"{name} must be >= {min_value}, got {value}")
    if max_value is not None and value > max_value:
        raise ValueError(f"{name} must be <= {max_value}, got {value}")
    return value


def validate_real(name: str, value: Any, *, finite: bool = True) -> float:
    """
    Validate that value is a real number (int/float) and optionally finite.
    
    Parameters
    ----------
    name : str
        The name of the parameter (for error messages).
    value : Any
        The value to validate.
    finite : bool, optional
        Whether to check if the value is finite (not inf/nan), by default True.
    
    Returns
    -------
    float
        The validated float value.
    
    Raises
    ------
    TypeError
        If value is not a real number (int or float).
    ValueError
        If finite=True and value is not finite.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}: {value!r}")
    value_f = float(value)
    if finite and not np.isfinite(value_f):
        raise ValueError(f"{name} must be finite, got {value_f}")
    return value_f


def validate_positive(name: str, value: Any) -> float:
    """
    Validate that value is a positive, finite real number.
    
    Parameters
    ----------
    name : str
        The name of the parameter (for error messages).
    value : Any
        The value to validate.
    
    Returns
    -------
    float
        The validated positive float value.
    
    Raises
    ------
    TypeError
        If value is not a real number.
    ValueError
        If value is not finite or not positive (> 0).
    """
    value_f = validate_real(name, value, finite=True)
    if value_f <= 0.0:
        raise ValueError(f"{name} must be > 0, got {value_f}")
    return value_f


def validate_xy_data(data: Any, *, min_rows: int = 2) -> np.ndarray:
    """
    Validate that data is numeric, array-like with shape (N, 2) (and finite).
    
    Parameters
    ----------
    data : Any
        Array-like data with shape (N, 2) representing (x, y) pairs.
    min_rows : int, optional
        Minimum number of rows required, by default 2.
    
    Returns
    -------
    np.ndarray
        Validated numpy array with shape (N, 2), suitable for downstream code.
    
    Raises
    ------
    ValueError
        If data is not 2D, doesn't have 2 columns, has fewer than min_rows rows,
        or contains NaN/infinite values.
    TypeError
        If data is not numeric.
    """
    arr = np.asarray(data)
    if arr.ndim != 2:
        raise ValueError(f"data must be 2D array-like with shape (N, 2), got ndim={arr.ndim}")
    if arr.shape[1] != 2:
        raise ValueError(f"data must have exactly 2 columns (x, y), got shape={arr.shape}")
    if arr.shape[0] < min_rows:
        raise ValueError(f"data must have at least {min_rows} rows, got {arr.shape[0]}")
    if not np.issubdtype(arr.dtype, np.number):
        raise TypeError(f"data must be numeric, got dtype={arr.dtype}")
    if not np.isfinite(arr).all():
        raise ValueError("data contains NaN or infinite values")
    return arr


def validate_rng_seed(seed: Optional[int] = None) -> np.random.Generator:
    """
    Return a numpy random number generator with optional seed validation.
    
    Parameters
    ----------
    seed : Optional[int], optional
        Random seed for reproducibility. If None, uses a random seed.
        Must be a non-negative integer if provided, by default None.
    
    Returns
    -------
    np.random.Generator
        A numpy random number generator instance.
    
    Raises
    ------
    TypeError
        If seed is provided but is not an integer.
    ValueError
        If seed is provided but is negative.
    
    Notes
    -----
    Use this function in public-facing functions to ensure reproducibility
    when needed while maintaining a consistent interface.
    """
    if seed is None:
        seed = int(np.random.default_rng().integers(0, 2**31 - 1))
    validate_int("seed", seed, min_value=0)
    return seed, np.random.default_rng(seed)


def save_array(data: np.ndarray, header: str,
               path: str = '../artifacts/simulated_data.csv') -> None:
    """
    Save a numpy array to a CSV file with a header.
    
    Parameters
    ----------
    data : np.ndarray
        The array data to save.
    header : str
        Column header(s) for the CSV file.
    path : str, optional
        File path where the CSV will be saved,
        by default '../artifacts/simulated_data.csv'.
    
    Returns
    -------
    None
    """
    np.savetxt(path, data, delimiter=',', header=header, comments='')