import glob
import os
import pathlib
import argparse
import sys
from importlib.util import module_from_spec, spec_from_file_location
from typing import Callable, List, Dict
from rich.console import Console
from rich.progress import Progress, TaskID

from dstest.fixtures import get_fixture
from dstest.results import DSResult, registry
from dstest.output import print_result_cli


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


def run_experiments_in_module(experiments: List[Callable], module: str, progress_bar: Progress, task: TaskID) \
        -> Dict[str, DSResult]:
    if len(experiments) == 0:
        return {}
    for experiment in experiments:
        progress_bar.update(
            task,
            description=f"Running {module.replace('.py', '')}.{experiment.__name__}..."
        )

        arguments = experiment.__code__.co_varnames[:experiment.__code__.co_argcount]
        experiment_inputs = {arg: get_fixture(arg) for arg in arguments}

        with registry.start_experiment(experiment.__name__, module_name=module):
            experiment(**experiment_inputs)
        progress_bar.advance(task, advance=1/(len(experiments)))


def find_modules(path_str: str) -> List[pathlib.Path]:
    path = pathlib.Path(path_str)
    if path.is_file():
        if path.suffix == '.py':
            experiment_files = [path]
        else:
            raise ValueError(f"The file {path} is not a Python (.py) file.")
    elif path.is_dir():
        pattern = os.path.join(path, '**', '*.py')
        experiment_file_strings = glob.glob(pattern, recursive=True)
        experiment_files = [pathlib.Path(file) for file in experiment_file_strings]
    else:
        raise ValueError(f"Path or File {path} does not exist.")
    return experiment_files


def run_modules(experiment_files: List[pathlib.Path]):
    console = Console()
    console.print(
        f"[bold blue] {'-' * 20} Running DSTest {'-' * 20} [/bold blue]")

    with Progress() as progress:
        task = progress.add_task("[cyan]Running experiments...", total=len(experiment_files))

        for file in experiment_files:
            progress.update(task, description=f"Running {file.name}...")
            experiment_functions = parse_experiments_from_file(file)
            if args.experiment is not None:
                experiment_functions = [
                    ex_func for ex_func in experiment_functions
                    if ex_func.__name__ in ["experiment_" + args.experiment, args.experiment]]
            if len(experiment_functions) > 0:
                run_experiments_in_module(experiment_functions, module=file.name, progress_bar=progress, task=task)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DSTest')
    parser.add_argument("-e", "--experiment", type=str, help='experiment function to run')
    parser.add_argument("path", type=str, help='Path to the file or directory to run DSTest on')
    args = parser.parse_args()

    run_modules(find_modules(args.path))
    print_result_cli()



