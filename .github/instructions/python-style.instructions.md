---
applyTo: "src/**/*.py"
---

## Python style conventions for this project

- Use **Google-style docstrings** with `Args:` and `Returns:` sections for all functions
- Type-annotate all function signatures; use `str | Path` for file path parameters and `tuple[np.ndarray, np.ndarray]` for multi-array returns
- All analysis functions take a `pd.DataFrame` (loaded via `read_expec`) or a `np.ndarray` — no raw file paths in analysis functions
- Do not leave `pass` placeholders; implement or raise `NotImplementedError`
- `moving_average` edge behaviour: use `pd.Series.rolling(center=True, min_periods=1)` — never pad with NaN
- FFT functions must subtract the mean before transforming to remove the DC offset
