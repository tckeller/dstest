import subprocess

def test_output():

    result = subprocess.run(
        ['python', "-m", "dstest",'tests/example_ds_code/linreg_example.py'],
            stdout=subprocess.PIPE,
            text=True
            )

    expected_output = """
    DSTest Results
    ==============================================
                        rmse
    test_0_poly_fit     2.997
    test_0_poly_fit     0.296
    ==============================================
    """

    # Use a simple assert statement for checking
    assert result.stdout == expected_output
