class DSResult():
    """ This class holds the result """
    def __init__(self, experiment_name=None, **kwargs):
        self.results = kwargs
        self.experiment_name = experiment_name

    def __repr__(self):
        return str(self.results)

    def get_metrics(self):
        return set(self.results.keys())