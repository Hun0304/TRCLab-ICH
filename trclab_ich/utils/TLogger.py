import os
import logging
import datetime

LOGGER_LEVEL = logging.DEBUG
PROJECT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
LOGS_DIR = os.path.join(PROJECT_DIR, "logs")


class TLogger:
    _instance = None

    @staticmethod
    def get_logger():
        if TLogger._instance is None:
            TLogger("TRCLab-ICH")
        return TLogger._instance

    def __init__(self, log_name):
        if TLogger._instance is not None:
            raise Exception('only one instance can exist')

        else:
            TLogger._instance = self
            log_filename = datetime.datetime.now().strftime(f"{log_name}-%Y-%m-%d_%H_%M_%S.log")
            formatter = logging.Formatter("%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d --- %(message)s",
                                          datefmt='%Y%m%d %H:%M:%S')
            self._logger = logging.getLogger(log_name)
            self._logger.setLevel(LOGGER_LEVEL)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(LOGGER_LEVEL)
            console_handler.setFormatter(formatter)
            file_handler = logging.FileHandler(os.path.join(LOGS_DIR, log_filename))
            file_handler.setLevel(LOGGER_LEVEL)
            file_handler.setFormatter(formatter)

            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    def debug(self, log_message):
        self._logging(log_message, logging.DEBUG)

    def info(self, log_message):
        self._logging(log_message, logging.INFO)

    def warning(self, log_message):
        self._logging(log_message, logging.WARNING)

    def error(self, log_message):
        self._logging(log_message, logging.ERROR)

    def critical(self, log_message):
        self._logging(log_message, logging.CRITICAL)

    def _logging(self, message, level):
        self._logger.log(level, message, stacklevel=3)

