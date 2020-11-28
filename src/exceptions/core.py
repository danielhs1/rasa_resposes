from src.exceptions import Error


class ElasticApmUrlIsRequired(Error):
    def __str__(self):
        return "elastic-apm-url-is-required-error"
