from fastapi import status


class AuthorizationError(Exception):
    """Base exception for authorization errors."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> None:
        """
        Initialize the AuthorizationError with a message and an optional status code.

        Args:
            message: The error message.
            status_code: The HTTP status code (default is 400).
        """
        super().__init__(message)
        self.status_code = status_code
