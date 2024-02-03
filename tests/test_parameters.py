import subprocess
import sys

def test_output_with_parameters():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/examples/linreg_example.py'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest -------------------- 
┌────────────────────────────────┬───────┬───────┐
│ Experiment                     │ mae   │ rmse  │
├────────────────────────────────┼───────┼───────┤
│ linreg_example                 │       │       │
│ 0_poly_fit                     │       │ 3.04  │
│ 1_poly_fit                     │ 0.025 │ 0.287 │
└────────────────────────────────┴───────┴───────┘
"""

    # Use a simple assert statement for checking
    assert result.stdout == expected_output