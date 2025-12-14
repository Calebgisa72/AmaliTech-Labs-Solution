class ImporterError(Exception):
    """Base class for all importer-related errors."""

    default_message = "An importer error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class FileFormatError(ImporterError):
    """Raised when the CSV file is malformed or missing required columns."""

    default_message = "CSV file format is invalid or corrupted."


class DuplicateUserError(ImporterError):
    """Raised when a duplicate user is detected."""

    default_message = "Duplicate user detected."


class StorageError(ImporterError):
    """Raised when an error occurs during storage operations."""

    default_message = "Storage operation failed."


class CSVFileNotFoundError(ImporterError):
    """Raised when the CSV file cannot be found."""

    default_message = "CSV file not found."
