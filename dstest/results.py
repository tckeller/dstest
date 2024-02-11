from typing import Any, Dict, Optional


class DSResult:
    """ This class holds the result """
    def __init__(self, module_name: str = "", experiment_name: str = None, docstring: str = ""):
        self.parameters = {}
        self.metrics = {}
        self.figures = {}
        self.docstring = docstring
        self.module_name = module_name
        self.experiment_name = experiment_name

    def __repr__(self):
        return str(self.parameters)

    def log_metrics(self, **metrics: Dict[str, Any]):
        self.metrics = {**self.metrics, **metrics}

    def log_parameters(self, **parameters: Dict[str, Any]):
        self.parameters = {**self.parameters, **parameters}

    def log_figures(self, **figures: Dict[str, Any]):
        self.figures = {**self.figures, **figures}

    def metric_names(self):
        return set(self.metrics.keys())

    def parameter_names(self):
        return set(self.parameters.keys())


class ResultRegistry:
    _instance: Optional["ResultRegistry"] = None
    _current_experiment: Optional[DSResult] = None
    _experiment_results = []

    def __new__(cls):
        """ The ResultRegistry is a Singleton """
        if cls._instance is None:
            cls._instance = super(ResultRegistry, cls).__new__(cls)
        return cls._instance

    def start_experiment(self, experiment_name: str, module_name: str = "", docstring: str = ""):
        self._current_experiment: DSResult = DSResult(
            experiment_name=experiment_name,
            module_name=module_name,
            docstring=docstring)
        return self

    def end_experiment(self):
        self._experiment_results.append(self._current_experiment)
        self._current_experiment = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_experiment()

    @staticmethod
    def check_experiment_set(func):
        def wrapper(self, *args, **kwargs):
            if self._current_experiment is None:
                raise AttributeError("No experiment currently started! use registry.start_experiment!")
            return func(self, *args, **kwargs)
        return wrapper

    @check_experiment_set
    def log_metrics(self, **metrics):
        self._current_experiment.log_metrics(**metrics)

    @check_experiment_set
    def log_parameters(self, **parameters):
        self._current_experiment.log_parameters(**parameters)

    @check_experiment_set
    def log_figures(self, **figures):
        self._current_experiment.log_figures(**figures)

    def all_metric_names(self):
        return set().union(*[result.metric_names() for result in self.experiment_results])

    def all_parameter_names(self):
        return set().union(*[result.parameter_names() for result in self.experiment_results])

    @property
    def experiment_results(self):
        return sorted(self._experiment_results, key=lambda x: (x.module_name, x.experiment_name))


registry = ResultRegistry()