import subprocess
import sys


def test_output():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/examples/linreg_example.py'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest Results from 2 Experiments -------------------- 
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
        [sys.executable, "-m", "dstest", 'tests/examples/linreg_example.py', '-e', '0_poly_fit'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest Results from 1 Experiments -------------------- 
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
        [sys.executable, "-m", "dstest", 'tests/examples/directory_example'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest Results from 2 Experiments -------------------- 
┌────────────────────────────────┬───────┬───────┐
│ Experiment                     │ mae   │ rmse  │
├────────────────────────────────┼───────┼───────┤
│ directory_example              │       │       │
│ 0_poly_fit                     │       │ 3.04  │
│ 1_poly_fit                     │ 0.025 │ 0.287 │
└────────────────────────────────┴───────┴───────┘
"""

    # Use a simple assert statement for checking
    assert result.stdout == expected_output


def test_output_with_parameters():
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/examples/parameter_example.py'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    expected_output = """ -------------------- DStest Results from 2 Experiments -------------------- 
┌────────────────────────────────┬───────┬─────┐
│ Experiment                     │ depth │ mae │
├────────────────────────────────┼───────┼─────┤
│ parameter_example              │       │     │
│ 0_poly_fit                     │ 6     │ 1.2 │
│ 1_poly_fit                     │ 12    │ 1.4 │
└────────────────────────────────┴───────┴─────┘
"""

    # Use a simple assert statement for checking
    assert result.stdout == expected_output
