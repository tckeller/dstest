from dstest.results import registry, ResultRegistry
import pytest

class TestResultRegistry:

    def test_singleton(self):
        instance1 = ResultRegistry()
        instance2 = ResultRegistry()

        assert instance1 is instance2

    def test_context_manager(self):
        with registry.start_experiment("my_experiment"):
            registry.log_metrics(my_metric=1.2)

        assert registry.experiment_results[0].experiment_name == "my_experiment"
        assert "my_metric" in registry.experiment_results[0].metrics
        assert registry.experiment_results[0].metrics["my_metric"] == 1.2

    def test_use_registry_directly(self):
        registry.start_experiment("my_experiment")
        registry.log_metrics(my_metric=1.2)
        registry.end_experiment()

        assert registry.experiment_results[0].experiment_name == "my_experiment"
        assert "my_metric" in registry.experiment_results[0].metrics
        assert registry.experiment_results[0].metrics["my_metric"] == 1.2

    def test_no_experiment_started_raises_error(self):
        with pytest.raises(AttributeError):
            registry.log_metrics(my_metric=1.2)
