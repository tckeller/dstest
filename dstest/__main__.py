import pathlib
import argparse
import logging
import sys
from importlib.util import module_from_spec, spec_from_file_location
from typing import Callable, List, Dict
from operator import itemgetter

from rich.console import Console
from rich.table import Table

from dstest.fixtures import fixture_registry
from dstest.results import DSResult
import functools

logger = logging.getLogger("DSTest")
logger.setLevel("INFO")


def import_pyfile_as_module(file_path: pathlib.Path):
    module_name = file_path.stem  # Get file name without suffix as module name
    spec = spec_from_file_location(module_name, file_path)
    module = module_from_spec(spec)
    sys.modules[module_name] = module  # Add to sys.modules
    spec.loader.exec_module(module)
    return module


def find_experiment_functions(module):
    experiment_functions = []
    for attr_name in dir(module):
        if attr_name.startswith('experiment_'):
            attr = getattr(module, attr_name)
            if callable(attr):
                experiment_functions.append(attr)
    return experiment_functions


def parse_experiments_from_file(file: pathlib.Path):
    module = import_pyfile_as_module(file)
    experiment_functions = find_experiment_functions(module)
    return experiment_functions


def run_experiments(experiments: List[Callable]) -> Dict[str, DSResult]:
    if len(experiments) == 0:
        return {}
    experiment = experiments.pop()
    arguments = experiment.__code__.co_varnames[:experiment.__code__.co_argcount]
    experiment_inputs = {arg: fixture_registry[arg]() for arg in arguments}
    result = experiment(**experiment_inputs)
    assert isinstance(result, DSResult), f"Function {experiment.__name__} did not return a DSResult!"
    return {**{experiment.__name__: result}, **run_experiments(experiments)}


def print_results(results, metrics, table):
    if len(results) == 0:
        return table
    module_name, module_results = results.pop()
    table.add_row(module_name.replace(".py", ""))
    table = print_experiment_results(list(module_results.items()), metrics, table)
    table = print_results(results, metrics, table)
    return table


def print_experiment_results(module_results, metrics, table):
    if len(module_results) == 0:
        return table
    experiment_name, experiment_results = module_results.pop()

    table.add_row(
        experiment_name.replace("experiment_", ""),
        *[str(experiment_results.results[metric]) for metric in metrics if metric in experiment_results.results])
    table = print_experiment_results(module_results, metrics, table)
    return table


def get_metrics(results):
    if len(results) == 0:
        return set()
    result_name, result_value = results.pop()
    if isinstance(result_value, dict):
        metrics = get_metrics(list(result_value.items()))
    elif isinstance(result_value, DSResult):
        metrics = result_value.get_metrics()
    else:
        metrics = set()
    return metrics.union(get_metrics(results))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DSTest')
    parser.add_argument('path', type=str, help='Path to the file or directory to run DSTest on')
    args = parser.parse_args()

    path = pathlib.Path(args.path)
    run_results = {}
    if path.is_file():
        if path.suffix == '.py':
            experiment_functions = parse_experiments_from_file(path)
            run_results[path.name] = run_experiments(experiment_functions)
        else:
            print(f"The file {path} is not a Python (.py) file.")
    else:
        print(f"File {path} does not exist.")
    metrics = list(get_metrics(list(run_results.items())))
    metrics.sort()

    console = Console()
    console.print(f"[bold blue] {'-'*20} DStest {'-'*20} [/bold blue]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Experiment", style="dim", width=30)
    for metric in metrics:
        table.add_column(metric)
    table = print_results(list(run_results.items()), metrics, table)

    console.print(table)


