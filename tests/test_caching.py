import subprocess
import sys
import time


def test_output():

    start = time.time()
    result = subprocess.run(
        [sys.executable, "-m", "dstest", 'tests/examples/cache_example.py'],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    end = time.time()

    assert end - start < 4
