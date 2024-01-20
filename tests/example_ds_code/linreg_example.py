"""
This file should show how I imagine a data science test should look like
"""
# from dstest import fixture, DSTestResult
import random
import numpy as np

fixture = lambda x: x

class DSTestResult:
    def __init__(self, **kwargs):
        self.results = kwargs

    def __repr__(self):
        return str(self.results)

def calculate_rmse(pred, truth):
    return np.sqrt((pred - truth).dot(pred - truth))


@fixture
def linear_dummy_data():
    """ Generate some linear data to run the tests on """
    random.seed = 12
    x = np.random.random(100)
    y = x + 0.1 * np.random.random(100)
    return x, y


def test_0_poly_fit(linear_dummy_data=linear_dummy_data()):
    x, y = linear_dummy_data
    c = np.polyfit(x, y, 0)
    model = lambda _: c[0]
    rmse = calculate_rmse(model(x), y)
    return DSTestResult(rmse=round(rmse, 3))


def test_1_poly_fit(linear_dummy_data=linear_dummy_data()):
    x, y = linear_dummy_data
    c = np.polyfit(x, y, 1)
    model = lambda _: c[1] + c[0]*x
    rmse = calculate_rmse(model(x), y)
    return DSTestResult(rmse=round(rmse, 3))


if __name__ == "__main__":
    result1 = test_0_poly_fit()
    result2 = test_1_poly_fit()
    print(result1, result2)