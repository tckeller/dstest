import subprocess
import sys


def test_output():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/linreg_example/linreg_example.py'],
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


def test_single_function():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/linreg_example/linreg_example.py', '-e', '0_poly_fit'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest -------------------- 
┌────────────────────────────────┬──────┐
│ Experiment                     │ rmse │
├────────────────────────────────┼──────┤
│ linreg_example                 │      │
│ 0_poly_fit                     │ 3.04 │
└────────────────────────────────┴──────┘
"""

    # Use a simple assert statement for checking
    assert result.stdout == expected_output


def test_output_from_dir():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/linreg_example'],
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
