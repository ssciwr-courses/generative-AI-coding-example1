# Agent Instructions

## Project overview
Python data-analysis project for quantum dynamics output files (e.g. `expec.t`).
All analysis code lives in `src/analyze_data.py`; tests live in `src/test/`.

## Environment
- Conda environment: `genai` — activate before running anything: `conda activate genai`
- Dependencies: `pandas`, `numpy`, `matplotlib`, `pytest` (see [requirements.txt](requirements.txt))
- Python 3.12

## Commands
| Task | Command |
|------|---------|
| Run analysis script | `python src/analyze_data.py` |
| Run all tests | `python -m pytest src/test/ -v` |
| Run single test file | `python -m pytest src/test/test_analyze_data.py -v` |

## Project structure
```
data/expec.t          # whitespace-delimited data file (time norm <x> <y> <z> <H>)
src/analyze_data.py   # all analysis functions
src/test/
  conftest.py         # adds src/ to sys.path so tests can import analyze_data
  test_analyze_data.py
```

## Conventions
- All functions in `src/analyze_data.py` take a `pd.DataFrame` (loaded via `read_expec`) or a `np.ndarray`
- Tests use plain `pytest` — no test class wrappers
- `conftest.py` in `src/test/` inserts `src/` into `sys.path`; keep it present when adding new test files
- `fourier_transform_z` subtracts the mean before FFT to remove the DC offset
- `moving_average` uses `pd.Series.rolling(center=True, min_periods=1)` — no NaN at edges
- Data file paths in tests are resolved relative to the test file using `Path(__file__).parents[n]`

## Data file format
`data/expec.t` is whitespace-delimited with a single header row:
```
time   norm   <x>   <y>   <z>   <H>
```
Read it with `read_expec(filepath)` from `analyze_data`.
