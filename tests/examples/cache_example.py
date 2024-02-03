from dstest import fixture, registry
import time


@fixture
def wait_2_seconds():
    time.sleep(2)


def experiment_cache_1(wait_2_seconds):
    registry.log_metrics(x=1)


def experiment_cache_2(wait_2_seconds):
    registry.log_metrics(x=1)