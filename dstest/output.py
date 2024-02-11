import csv
from typing import List

from rich.console import Console
from rich.style import Style
from rich.table import Table

from dstest.results import DSResult, registry


def append_results_to_table(metrics: List[str], parameters: List[str], table: Table):
    blue_style = Style(color="turquoise2")

    current_module = None
    for result in registry.experiment_results:
        if result.module_name != current_module:
            table.add_row(result.module_name.replace(".py", ""), style=blue_style)
            current_module = result.module_name

        table.add_row(
            "    " + result.experiment_name.replace("experiment_", ""),
            *map(lambda p: str(result.parameters.get(p, "")), parameters),
            *map(lambda m: str(result.metrics.get(m, "")), metrics),
        )

    return table


def print_result_cli():
    metrics = sorted(registry.all_metric_names())
    parameters = sorted(registry.all_parameter_names())

    console = Console()
    console.print(f"[bold blue] {'-'*20} DStest Results from {len(registry.experiment_results)} Experiments {'-'*20} [/bold blue]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Experiment", style="dim", width=30)

    [table.add_column(parameter) for parameter in parameters]
    [table.add_column(metric) for metric in metrics]

    table = append_results_to_table(metrics, parameters, table)

    console.print(table)


def print_result_file(file_path: str):
    metrics = sorted(registry.all_metric_names())
    parameters = sorted(registry.all_parameter_names())

    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["experiment"] + parameters + metrics)

        for result in registry.experiment_results:
            module = result.module_name.replace(".py", "")

            csv_writer.writerow([
                module + "." + result.experiment_name.replace("experiment_", ""),
                *map(lambda p: str(result.parameters.get(p, "")), parameters),
                *map(lambda m: str(result.metrics.get(m, "")), metrics),
            ])
