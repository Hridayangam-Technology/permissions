from abc import ABC, abstractmethod
from permission_manager.core.types import UserIdType
from permission_manager.core.permission import Permission


class PermissionDelegate(ABC):
    """Abstract base class for getting user permissions."""

    @abstractmethod
    async def get_permissions(self, user_id: UserIdType) -> list[Permission]:
        """
        Get permissions for a user.

        Args:
            user_id: User identifier

        Returns:
            List of Permission objects
        """
        pass

    @abstractmethod
    async def validate_user(self, user_id: UserIdType) -> bool:
        """
        Validate if the user with the given user_id exists and is authorized.

        Args:
            user_id: User identifier to validate

        Returns:
            True if the user is valid, False otherwise
        """
        pass
