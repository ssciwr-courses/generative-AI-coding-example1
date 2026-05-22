import numpy as np
import pytest
import pandas as pd
from pathlib import Path

from analyze_data import fourier_transform_z, get_z_and_H, moving_average, read_expec

DATA_FILE = Path(__file__).parents[2] / "data" / "expec.t"


def test_read_expec_returns_dataframe():
    df = read_expec(DATA_FILE)
    assert isinstance(df, pd.DataFrame)


def test_read_expec_columns():
    df = read_expec(DATA_FILE)
    expected_columns = ["time", "norm", "<x>", "<y>", "<z>", "<H>"]
    assert list(df.columns) == expected_columns


def test_read_expec_first_row():
    df = read_expec(DATA_FILE)
    assert df["time"].iloc[0] == pytest.approx(0.0)
    assert df["norm"].iloc[0] == pytest.approx(1.0)


def test_read_expec_not_empty():
    df = read_expec(DATA_FILE)
    assert len(df) > 0


# --- get_z_and_H ---


def test_get_z_and_H_returns_numpy_arrays():
    df = read_expec(DATA_FILE)
    z, H = get_z_and_H(df)
    assert isinstance(z, np.ndarray)
    assert isinstance(H, np.ndarray)


def test_get_z_and_H_correct_length():
    df = read_expec(DATA_FILE)
    z, H = get_z_and_H(df)
    assert len(z) == len(df)
    assert len(H) == len(df)


def test_get_z_and_H_values_match_dataframe():
    df = read_expec(DATA_FILE)
    z, H = get_z_and_H(df)
    np.testing.assert_array_equal(z, df["<z>"].to_numpy())
    np.testing.assert_array_equal(H, df["<H>"].to_numpy())


# --- moving_average ---


def test_moving_average_same_length():
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = moving_average(arr, window=3)
    assert len(result) == len(arr)


def test_moving_average_no_nan():
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = moving_average(arr, window=3)
    assert not np.any(np.isnan(result))


def test_moving_average_interior_values():
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = moving_average(arr, window=3)
    # Interior values: mean of [1,2,3]=2, [2,3,4]=3, [3,4,5]=4
    np.testing.assert_allclose(result[1:-1], [2.0, 3.0, 4.0])


def test_moving_average_window_1_is_identity():
    arr = np.array([1.0, 3.0, 5.0, 7.0])
    result = moving_average(arr, window=1)
    np.testing.assert_array_equal(result, arr)


def test_moving_average_invalid_window():
    with pytest.raises(ValueError):
        moving_average(np.array([1.0, 2.0]), window=0)


# ---------------------------------------------------------------------------
# Behaviour test
# Feature: As a researcher, I want to compute the Fourier transform of the
#          position expectation value, so that I can determine the frequency
#          of the oscillation.
#
# Scenario: Dominant frequency recovered from a known signal
# ---------------------------------------------------------------------------


def test_fourier_transform_recovers_dominant_frequency():
    """
    GIVEN a position expectation value sampled at 0.1 fs intervals
          that contains a dominant oscillation at 0.25 fs^-1
    WHEN  the researcher computes the Fourier transform of the position column
    THEN  the resulting spectrum has its peak at 0.25 fs^-1 within tolerance 0.01
    AND   the peak amplitude exceeds the noise floor by at least a factor of 10
    """
    # GIVEN
    dt = 0.1  # sampling interval [fs]
    n = 1000  # points -> frequency resolution df = 1/(n*dt) = 0.01 fs^-1
    target_freq = 0.25  # fs^-1  (falls exactly on a bin with this resolution)
    time = np.arange(n) * dt
    rng = np.random.default_rng(42)
    signal = 5.0 * np.sin(2 * np.pi * target_freq * time) + 0.1 * rng.normal(size=n)
    df = pd.DataFrame({"time": time, "<z>": signal})

    # WHEN
    freqs, amplitudes = fourier_transform_z(df)

    # THEN - peak is at 0.25 fs^-1 within tolerance 0.01
    peak_idx = np.argmax(amplitudes)
    peak_freq = freqs[peak_idx]
    assert abs(peak_freq - target_freq) <= 0.01, (
        f"Peak frequency {peak_freq:.4f} fs^-1 not within 0.01 of {target_freq} fs^-1"
    )

    # AND - peak amplitude exceeds noise floor by at least a factor of 10
    peak_amp = amplitudes[peak_idx]
    noise_mask = np.ones(len(freqs), dtype=bool)
    noise_mask[peak_idx] = False
    noise_floor = np.mean(amplitudes[noise_mask])
    assert peak_amp / noise_floor >= 10, (
        f"Peak-to-noise ratio {peak_amp / noise_floor:.1f} is less than 10"
    )
