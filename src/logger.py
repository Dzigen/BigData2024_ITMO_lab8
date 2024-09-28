import logging
import os
import sys
import functools

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = os.path.join(os.getcwd(), "logfile.log")


class Logger:
    """
        Class for logging behaviour of data exporting - object of ExportingTool class
    """

    def __init__(self, show: bool) -> None:
        self.show = show

    def get_console_handler(self) -> logging.StreamHandler:
        """
            Class method the aim of which is getting a console handler to show logs on terminal

        Returns:
            logging.StreamHandler: handler object for streaming output through terminal
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler

    def get_file_handler(self) -> logging.FileHandler:
        """
            Class method the aim of which is getting a file handler to write logs in file LOG_FILE

        Returns:
            logging.FileHandler: handler object for streaming output through std::filestream
        """
        file_handler = logging.FileHandler(LOG_FILE, mode='w')
        file_handler.setFormatter(FORMATTER)
        return file_handler

    def get_logger(self, logger_name: str):
        """
            Class method which creates logger with certain name

        Args:
            logger_name (str): name for logger

        Returns:
            logger: object of Logger class
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        if self.show:
            logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger

    @staticmethod
    def cls_se_log(info: str):
        """Декаратор с аргументами для логирования старта и завершения работы вложенного метода

        Args:
            info (str): _description_
        """
        def wrap(func):
            @functools.wraps(func)
            def wrapped_f(self, *args, **kwargs):
                self.log.info('START_METHOD: ' + info)
                value = func(self, *args, **kwargs)
                self.log.info('END_METHOD: ' + info)
                return value
            return wrapped_f
        return wrap


if __name__ == "__main__":
    pass
