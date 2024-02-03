from typing import List

from rich.console import Console
from rich.style import Style
from rich.table import Table

from dstest.results import DSResult, registry


def print_registry_cli(experiment_results: List[DSResult], metrics: List[str], parameters: List[str], table: Table):
    sort_results_by_module = sorted(experiment_results, key=lambda x: (x.module_name, x.experiment_name))
    blue_style = Style(color="turquoise2")

    current_module = None
    for result in sort_results_by_module:
        if result.module_name != current_module:
            table.add_row(result.module_name.replace(".py", ""), style=blue_style)
            current_module = result.module_name

        table.add_row(
            result.experiment_name.replace("experiment_", ""),
            *map(lambda m: str(result.parameters.get(m, "")), parameters),
            *map(lambda m: str(result.metrics.get(m, "")), metrics),
        )

    return table


def print_result_cli():
    metrics = list(registry.all_metric_names())
    metrics.sort()

    parameters = list(registry.all_parameter_names())
    parameters.sort()

    console = Console()
    console.print(f"[bold blue] {'-'*20} DStest {'-'*20} [/bold blue]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Experiment", style="dim", width=30)

    [table.add_column(parameter) for parameter in parameters]
    [table.add_column(metric) for metric in metrics]

    table = print_registry_cli(registry.experiment_results, metrics, parameters, table)

    console.print(table)

