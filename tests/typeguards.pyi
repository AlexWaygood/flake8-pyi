# flags: --extend-select=Y092

import builtins
import typing
from typing import Any

def is_awaitable(obj: object) -> bool: ...  # Y092 Consider using "typing_extensions.TypeGuard" as the return annotation for "is_awaitable"
def _is_int(obj: Any, /, *, positive: bool = False) -> bool: ...  # Y092 Consider using "typing_extensions.TypeGuard" as the return annotation for "is_int"
def isastring(obj: builtins.object, /) -> bool: ...  # Y092 Consider using "typing_extensions.TypeGuard" as the return annotation for "isastring"
def _is____908765complex(__obj: typing.Any) -> bool: ...  # Y092 Consider using "typing_extensions.TypeGuard" as the return annotation for "_is____908765complex" 

# Don't flag functions where the first parameter is annotated with something that's not `object` or `Any`
def is_positive(obj: int) -> bool: ...

# Don't flag functions that don't start with "is" or "_is"
def doesntstartwithis(obj: object) -> bool: ...

# Don't flag a function that's just "is_"
def is_(obj: object) -> bool: ...

# Doesn't matter how many underscores you have:
def _is_____(obj: Any, /) -> bool: ...

