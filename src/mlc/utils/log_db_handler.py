import logging

from mlc.db.manager import DbManager
from mlc.db.model.logs import LogRecord


class DatabaseLogHandler(logging.Handler):
    def __init__(self, db_manager: DbManager):
        super().__init__()
        self.db_manager = db_manager

    def emit(self, record):
        with self.db_manager.get_session() as session:
            log = LogRecord(
                level=record.levelname,
                name=record.name,
                message=record.getMessage(),
                pathname=record.pathname,
                lineno=record.lineno,
                func=record.funcName,
                exception=self.formatException(record.exc_info) if record.exc_info else None,
            )
            session.add(log)
