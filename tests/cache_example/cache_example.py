
import numpy.random
from dstest import fixture, DSResult
import numpy as np
import time


@fixture
def wait_2_seconds():
    time.sleep(2)


def experiment_cache_1(wait_2_seconds):
    return DSResult(x=1)


def experiment_cache_2(wait_2_seconds):
    return DSResult(x=1)