import logging

from django.test import TestCase


class LogTest(TestCase):
    LOGGER_NAME = "test_logger"
    LOG_MESSAGE = "This is a test message!"
    LOG_LEVEL_DEBUG = "DEBUG"
    LOG_LEVEL_INFO = "INFO"
    LOG_LEVEL_WARNING = "WARNING"
    LOG_LEVEL_ERROR = "ERROR"
    LOG_LEVEL_CRITICAL = "CRITICAL"

    def setUp(self):
        self.logger = logging.getLogger(self.LOGGER_NAME)

    def test_create_debug_log(self):
        """Check whether a debug log is created."""
        with self.assertLogs(logger=self.LOGGER_NAME, level=self.LOG_LEVEL_DEBUG) as logs_context_manager:
            self.logger.debug(self.LOG_MESSAGE)
        last_logged_message = logs_context_manager.output[-1]
        expected_message = self._build_expected_log_output(
            self.LOGGER_NAME, self.LOG_LEVEL_DEBUG, self.LOG_MESSAGE
        )
        self.assertEquals(last_logged_message, expected_message, "Last log is a properly formatted debug log")

    def test_create_info_log(self):
        """Check whether an info log is created."""
        with self.assertLogs(logger=self.LOGGER_NAME, level=self.LOG_LEVEL_INFO) as logs_context_manager:
            self.logger.info(self.LOG_MESSAGE)
        last_logged_message = logs_context_manager.output[-1]
        expected_message = self._build_expected_log_output(
            self.LOGGER_NAME, self.LOG_LEVEL_INFO, self.LOG_MESSAGE
        )
        self.assertEquals(last_logged_message, expected_message, "Last log is a properly formatted info log")

    def test_create_warning_log(self):
        """Check whether a warning log is created."""
        with self.assertLogs(logger=self.LOGGER_NAME, level=self.LOG_LEVEL_WARNING) as logs_context_manager:
            self.logger.warning(self.LOG_MESSAGE)
        last_logged_message = logs_context_manager.output[-1]
        expected_message = self._build_expected_log_output(
            self.LOGGER_NAME, self.LOG_LEVEL_WARNING, self.LOG_MESSAGE
        )
        self.assertEquals(
            last_logged_message, expected_message, "Last log is a properly formatted warning log"
        )

    def test_create_error_log(self):
        """Check whether an error log is created."""
        with self.assertLogs(logger=self.LOGGER_NAME, level=self.LOG_LEVEL_ERROR) as logs_context_manager:
            self.logger.error(self.LOG_MESSAGE)
        last_logged_message = logs_context_manager.output[-1]
        expected_message = self._build_expected_log_output(
            self.LOGGER_NAME, self.LOG_LEVEL_ERROR, self.LOG_MESSAGE
        )
        self.assertEquals(last_logged_message, expected_message, "Last log is a properly formatted error log")

    def test_create_critical_log(self):
        """Check whether a critical log is created."""
        with self.assertLogs(logger=self.LOGGER_NAME, level=self.LOG_LEVEL_CRITICAL) as logs_context_manager:
            self.logger.critical(self.LOG_MESSAGE)
        last_logged_message = logs_context_manager.output[-1]
        expected_message = self._build_expected_log_output(
            self.LOGGER_NAME, self.LOG_LEVEL_CRITICAL, self.LOG_MESSAGE
        )
        self.assertEquals(
            last_logged_message, expected_message, "Last log is a properly formatted critical log"
        )

    def _build_expected_log_output(self, logger: str, level: str, message: str) -> str:
        """Builds an expected log output in the following format:
        '*level*:*logger*:*message*'
        Example: 'ERROR:test_logger:This is a test message!'"""
        return f"{level}:{logger}:{message}"
