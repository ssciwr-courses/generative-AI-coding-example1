---
name: add-analysis-function
description: Scaffold a new analysis function and its tests following project conventions
---

Add a new analysis function to `src/analyze_data.py` and corresponding tests in `src/test/test_analyze_data.py`.

**Function to add:** $FUNCTION_DESCRIPTION

Follow these conventions:
- The function must accept a `pd.DataFrame` (from `read_expec`) or a `np.ndarray` as input
- Use Google-style docstring with Args and Returns sections
- Place the function in `src/analyze_data.py` alongside the existing functions
- Write at least 3 pytest tests covering: return type/shape, a known computed value, and an edge/error case
- Import the new function in `test_analyze_data.py` alongside the existing imports
- Data file paths in tests must use `Path(__file__).parents[2] / "data" / "expec.t"`

After implementing, run `python -m pytest src/test/test_analyze_data.py -v` to confirm all tests pass.
