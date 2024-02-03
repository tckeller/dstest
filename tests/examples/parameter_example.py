"""
This file should show how I imagine a data science test should look like
"""
from dstest import registry
import numpy as np


def experiment_0_poly_fit():
    registry.log_parameters(depth=6)
    registry.log_metrics(mae=1.2)


def experiment_1_poly_fit():
    registry.log_parameters(depth=12)
    registry.log_metrics(mae=1.4)
