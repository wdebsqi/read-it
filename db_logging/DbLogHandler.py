from logging import Formatter, Handler, LogRecord

formatter = Formatter()


class DbLogHandler(Handler):
    def emit(self, record: LogRecord):
        from .models import Log

        message = str(record.msg)

        if record.exc_info:
            message += formatter.formatException(record.exc_info)

        Log.objects.create(
            level=record.levelname,
            path=f"{record.pathname}:{record.lineno}",
            message=f"{message}",
        )
