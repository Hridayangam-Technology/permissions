from enum import Enum
from functools import wraps
from typing import Any, Callable

from permission_manager.core.types import PayloadType, UserIdType
from permission_manager.core.permission import Permission
from permission_manager.core.exception import AuthorizationError
from permission_manager.decorators.base import PermissionDelegate


def check_permissions[T: Enum, V: Enum](
    permissions: list[Permission],
    required_permissions: list[tuple[T, set[V]]],
) -> bool:
    """
    Check if granted permissions satisfy all the required permissions.

    Args:
        permissions: List of granted Permission objects
        required_permissions: List of required permissions, each containing a resource and a set of actions.

    Returns:
        True if all required permissions are granted; False otherwise.
    """
    for req_resource, req_actions in required_permissions:
        if not any(
            perm.resource == req_resource and req_actions.issubset(perm.actions)
            for perm in permissions
        ):
            return False
    return True


def extract_user_id(payload: PayloadType, kwargs: dict) -> UserIdType:
    """
    Extract the user ID from the payload or kwargs (typically from the request).

    Args:
        payload: Request payload which may contain user identification attributes.
        kwargs: Additional arguments which may contain user identification information.

    Returns:
        The extracted user ID.

    Raises:
        AuthorizationError: If no user ID is found in the request (either payload or kwargs).
    """
    if payload:
        for attr in ("admin_id", "user_id", "id"):
            user_id = getattr(payload, attr, None)
            if user_id is not None:
                return user_id

    for key in ("user_id", "admin_id"):
        if key in kwargs:
            return kwargs[key]

    raise AuthorizationError("No user ID found in request")


def require_permissions[T: Enum, V: Enum](
    required_permissions: list[tuple[T, set[V]]],
    delegate: PermissionDelegate,
) -> Callable:
    """
    Decorator factory for permission-based access control.

    This decorator checks if the user has the required permissions before executing the decorated function.

    Args:
        required_permissions: List of (resource, action) pairs required for access.
        delegate: An instance of PermissionDelegate to fetch and validate the user's permissions.

    Example:
        >>> @require_permissions([(Resource.USER, Action.READ)], delegate)
        ... async def get_user(user_id: UUID):
        ...     return await fetch_user(user_id)

    Returns:
        A decorator function that adds permission checks to the decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, payload: PayloadType, **kwargs: Any) -> Any:
            try:
                user_id = extract_user_id(payload, kwargs)

                if not await delegate.validate_user(user_id):
                    raise AuthorizationError("Unauthorized user")

                permissions = await delegate.get_permissions(user_id)
                if not check_permissions(permissions, required_permissions):
                    raise AuthorizationError("Insufficient permissions")

                return await func(*args, payload=payload, **kwargs)

            except AuthorizationError:
                raise
            except Exception as e:
                raise AuthorizationError(f"Authorization failed: {str(e)}")

        return wrapper

    return decorator
