from datetime import datetime


class Logger:

    def __init__(self, logName: str = "CarFactory"):
        self._logName = logName

    def logInfo(self, message: str) -> None:
        """Логирование информационного сообщения"""
        self._writeLog("INFO", message)

    def logWarning(self, message: str) -> None:
        """Логирование предупреждения"""
        self._writeLog("WARNING", message)

    def logError(self, message: str) -> None:
        """Логирование ошибки"""
        self._writeLog("ERROR", message)

    def logDebug(self, message: str) -> None:
        """Логирование отладочной информации"""
        self._writeLog("DEBUG", message)

    def _writeLog(self, level: str, message: str) -> None:
        """Запись лога"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logEntry = f"[{timestamp}] [{level}] {self._logName}: {message}"
        print(logEntry)