class Error(Exception):
    data = {}
    event_code = None
    exception = None

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.data = kwargs.get("data")
        self.exception = kwargs.get("exception")


class HttpError(Error):
    status_code = None

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status_code = kwargs.get("status_code")
