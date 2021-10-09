import threading


class ThreadWithLoggedException(threading.Thread):
    """
    Similar to Thread but will log exceptions to passed logger.

    Args:
        logger: Logger instance used to log any exception in child thread

    Exception is also reachable via <thread>.exception from the main thread.
    """

    DIVIDER = "*"*80

    def __init__(self, *args, **kwargs):
        try:
            self.logger = kwargs.pop("logger")
        except KeyError:
            raise Exception("Missing 'logger' in kwargs")
        super().__init__(*args, **kwargs)
        self.exception = None

    def run(self):
        try:
            if self._target is not None:
                self._target(*self._args, **self._kwargs)
        except Exception as exception:
            thread = threading.current_thread()
            self.exception = exception
            self.logger.exception(f"{self.DIVIDER}\nException in child thread {thread}: {exception}\n{self.DIVIDER}")
        finally:
            del self._target, self._args, self._kwargs


class WebsocketServerThread(ThreadWithLoggedException):
    """Dummy wrapper to make debug messages a bit more readable"""
    pass
