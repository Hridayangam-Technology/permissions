from typing import Any, Callable
from uuid import UUID
from typing_extensions import TypeAlias

UserIdType: TypeAlias = UUID | str | int
PayloadType: TypeAlias = Any | None
DecoratedCallable: TypeAlias = Callable[..., Any]
