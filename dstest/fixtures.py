fixture_registry = {}


def fixture(func):
    fixture_registry[func.__name__] = func
    return func


def get_fixture(name):
    return fixture_registry.get(name)