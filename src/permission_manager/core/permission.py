from enum import Enum


class Permission[ResourceType: Enum, ActionType: Enum]:
    """
    Generic Permission class that works with any Resource and Action enums.
    This class represents a permission, which grants a user specific actions on a resource.

    Example:
        >>> class UserResource(Enum):
        ...     PROFILE = "profile"
        >>> class UserAction(Enum):
        ...     VIEW = "view"
        >>> permission = Permission(UserResource.PROFILE, {UserAction.VIEW})
    """

    def __init__(self, resource: ResourceType, actions: set[ActionType]) -> None:
        self.resource = resource
        self.actions = actions

    def __repr__(self) -> str:
        return f"Permission(resource={self.resource}, actions={self.actions})"
