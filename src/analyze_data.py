import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


def read_expec(filepath: str | Path) -> pd.DataFrame:
    """Read the expec.t data file into a DataFrame.

    The file is whitespace-delimited with a single header row containing
    the column names: time, norm, <x>, <y>, <z>, <H>.

    Args:
        filepath: Path to the expec.t file.

    Returns:
        DataFrame with columns: time, norm, <x>, <y>, <z>, <H>.
    """
    return pd.read_csv(filepath, sep=r"\s+", engine="python")


def plot_expec(df: pd.DataFrame) -> None:
    """Plot <z> and <H> vs time from the expec.t data.

    Args:
        df: DataFrame containing the expec.t data.
    """
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

    axes[0].plot(df["time"], df["<z>"])
    axes[0].set_ylabel("<z>")
    axes[0].set_title("Expectation values vs time")

    axes[1].plot(df["time"], df["<H>"])
    axes[1].set_ylabel("<H>")
    axes[1].set_xlabel("time")

    fig.tight_layout()
    plt.show()


def plot_moving_average(df: pd.DataFrame, window: int = 5) -> None:
    """Plot <z> and <H> with their moving averages vs time.

    Args:
        df: DataFrame containing the expec.t data.
        window: Moving average window size.
    """
    time = df["time"].to_numpy()
    z, H = df["<z>"].to_numpy(), df["<H>"].to_numpy()
    z_avg = moving_average(z, window)
    H_avg = moving_average(H, window)

    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

    axes[0].plot(time, z, alpha=0.4, label="<z>")
    axes[0].plot(time, z_avg, label=f"moving avg (w={window})")
    axes[0].set_ylabel("<z>")
    axes[0].set_title("Expectation values with moving average")
    axes[0].legend()

    axes[1].plot(time, H, alpha=0.4, label="<H>")
    axes[1].plot(time, H_avg, label=f"moving avg (w={window})")
    axes[1].set_ylabel("<H>")
    axes[1].set_xlabel("time")
    axes[1].legend()

    fig.tight_layout()
    plt.show()


def get_z_and_H(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Extract <z> and <H> columns as numpy arrays.

    Args:
        df: DataFrame containing the expec.t data.

    Returns:
        Tuple of (z, H) as 1-D numpy arrays.
    """
    return df["<z>"].to_numpy(), df["<H>"].to_numpy()


def mean_H(df: pd.DataFrame) -> float:
    """Compute the mean of the <H> column.

    Args:
        df: DataFrame containing the expec.t data.

    Returns:
        Mean value of <H> as a float.
    """
    return float(df["<H>"].mean())


def moving_average(arr: np.ndarray, window: int) -> np.ndarray:
    """Compute a centered moving average of a 1-D array.

    At the edges where fewer than ``window`` neighbours are available,
    the average is computed over however many points exist (no NaN padding).

    Args:
        arr: Input 1-D array.
        window: Number of points to average over (must be >= 1).

    Returns:
        Array of the same length as ``arr`` with the moving average values.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    return pd.Series(arr).rolling(window, center=True, min_periods=1).mean().to_numpy()


def fourier_transform_z(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Compute the one-sided Fourier transform of the <z> values.

    Args:
        df: DataFrame containing the expec.t data with a uniform time step.

    Returns:
        Tuple of (frequencies, amplitudes) for the positive-frequency half.
    """
    z = df["<z>"].to_numpy() - df["<z>"].mean()  # remove DC offset
    dt = df["time"].iloc[1] - df["time"].iloc[0]
    n = len(z)
    freqs = np.fft.rfftfreq(n, d=dt)
    amplitudes = np.abs(np.fft.rfft(z)) / n
    return freqs, amplitudes


def plot_fourier_z(df: pd.DataFrame) -> None:
    """Plot the Fourier transform amplitude spectrum of <z>.

    Args:
        df: DataFrame containing the expec.t data.
    """
    freqs, amplitudes = fourier_transform_z(df)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(freqs, amplitudes)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Amplitude")
    ax.set_title("Fourier transform of <z>")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage
    expec_df = read_expec("data/expec.t")
    print(expec_df.head())
    plot_expec(expec_df)
    z, H = get_z_and_H(expec_df)
    print("z:", z)
    print("H:", H)
    z_avg = moving_average(z, window=5)
    H_avg = moving_average(H, window=5)
    print("z moving average:", z_avg)
    print("H moving average:", H_avg)
    plot_moving_average(expec_df, window=5)
    plot_fourier_z(expec_df)
