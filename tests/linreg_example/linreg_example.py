"""
This file should show how I imagine a data science test should look like
"""
import numpy.random

from dstest import fixture, DSResult
import numpy as np


def calculate_rmse(pred, truth):
    return np.sqrt((pred - truth).dot(pred - truth))


def calculate_mae(pred, truth):
    return np.abs(pred - truth).mean()


@fixture
def linear_dummy_data():
    """ Generate some linear data to run the tests on """
    numpy.random.seed(12)
    x = np.random.random(100)
    y = x + 0.1 * np.random.random(100)
    return x, y


def experiment_0_poly_fit(linear_dummy_data):
    x, y = linear_dummy_data
    c = np.polyfit(x, y, 0)
    model = lambda _: c[0]
    rmse = calculate_rmse(model(x), y)
    return DSResult(rmse=round(rmse, 3))


def experiment_1_poly_fit(linear_dummy_data):
    x, y = linear_dummy_data
    c = np.polyfit(x, y, 1)
    model = lambda _: c[1] + c[0]*x
    rmse = calculate_rmse(model(x), y)
    mae = calculate_mae(model(x), y)
    return DSResult(rmse=round(rmse, 3), mae=round(mae, 3))
