fixture_registry = {}
fixture_cache = {}


def fixture(func):
    fixture_registry[func.__name__] = func
    return func


def get_fixture(name):
    if name not in fixture_cache:
        fixture_cache[name] = fixture_registry.get(name)()
    return fixture_cache[name]