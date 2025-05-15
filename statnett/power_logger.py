"""With some extra time, I wanted to have some proper logging and added this setup"""

import datetime
import logging


class PowerDataLoggingFormatter(logging.Formatter):
    COLORS = {
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[91m",  # Red
    }
    RESET = "\033[0m"
    LEVEL_PADDING = 8  # Ensures consistent spacing for log level labels

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger_name = f"[{record.name}]".ljust(self.LEVEL_PADDING)
        level = f"[{record.levelname}]".ljust(self.LEVEL_PADDING + 2)
        log_msg = f"{logger_name} [{timestamp}] {level} | {record.getMessage()}"
        return f"{log_color}{log_msg}{self.RESET}"


class PowerDataLogger:
    def __init__(self, name, level):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        handler = logging.StreamHandler()
        handler.setFormatter(PowerDataLoggingFormatter())

        self.logger.addHandler(handler)

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def warning(self, message, *args):
        self.logger.warning(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def critical(self, message, *args):
        self.logger.critical(message, *args)
