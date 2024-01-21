import subprocess
import sys


def test_output():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/example_ds_code/linreg_example.py'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest -------------------- 
┌────────────────────────────────┬───────┐
│ Experiment                     │ rmse  │
├────────────────────────────────┼───────┤
│ linreg_example.py              │       │
│ 0_poly_fit                     │ 3.04  │
│ 1_poly_fit                     │ 0.287 │
└────────────────────────────────┴───────┘
"""

    # Use a simple assert statement for checking
    assert result.stdout == expected_output
