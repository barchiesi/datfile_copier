import sys
from enum import IntEnum


class LogLevel(IntEnum):
    ERROR = 1
    INFO = 2
    DEBUG = 3


class LevelLogger:

    class __Logger:

        level = LogLevel.ERROR

        def __str__(self):
            return repr(self) + self.level

        def set_level(self, logLevel):
            self.level = logLevel

        def info(self, msg):
            if self.level >= LogLevel.INFO:
                sys.stdout.write(f'INFO: {msg}\n')

        def debug(self, msg):
            if self.level >= LogLevel.DEBUG:
                sys.stdout.write(f'DEBUG: {msg}\n')

        def error(self, msg):
            if self.level >= LogLevel.ERROR:
                sys.stderr.write(f'ERROR: {msg}\n')


    instance = None

    def __getattr__(self, name):
        if not LevelLogger.instance:
            LevelLogger.instance = LevelLogger.__Logger()
        return getattr(self.instance, name)


Logger = LevelLogger()
