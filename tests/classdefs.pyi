import abc
import builtins
import collections.abc
import typing
import typing_extensions
from abc import abstractmethod
from collections.abc import AsyncIterator, Iterator
from typing import Any, overload

from _typeshed import Self
from typing_extensions import final

class Bad(object):  # Y040 Do not inherit from "object" explicitly, as it is redundant in Python 3
    def __new__(cls, *args: Any, **kwargs: Any) -> Bad: ...  # Y034 "__new__" methods usually return "self" at runtime. Consider using "_typeshed.Self" in "Bad.__new__", e.g. "def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self: ..."
    def __repr__(self) -> str: ...  # Y029 Defining __repr__ or __str__ in a stub is almost always redundant
    def __str__(self) -> builtins.str: ...  # Y029 Defining __repr__ or __str__ in a stub is almost always redundant
    def __eq__(self, other: Any) -> bool: ...  # Y032 Prefer "object" to "Any" for the second parameter in "__eq__" methods
    def __ne__(self, other: typing.Any) -> typing.Any: ...  # Y032 Prefer "object" to "Any" for the second parameter in "__ne__" methods
    def __enter__(self) -> Bad: ...  # Y034 "__enter__" methods in classes like "Bad" usually return "self" at runtime. Consider using "_typeshed.Self" in "Bad.__enter__", e.g. "def __enter__(self: Self) -> Self: ..."
    async def __aenter__(self) -> Bad: ...  # Y034 "__aenter__" methods in classes like "Bad" usually return "self" at runtime. Consider using "_typeshed.Self" in "Bad.__aenter__", e.g. "async def __aenter__(self: Self) -> Self: ..."
    def __iadd__(self, other: Bad) -> Bad: ...  # Y034 "__iadd__" methods in classes like "Bad" usually return "self" at runtime. Consider using "_typeshed.Self" in "Bad.__iadd__", e.g. "def __iadd__(self: Self, other: Bad) -> Self: ..."

class AlsoBad(int, builtins.object): ...  # Y040 Do not inherit from "object" explicitly, as it is redundant in Python 3

class Good:
    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self: ...
    @abstractmethod
    def __str__(self) -> str: ...
    @abc.abstractmethod
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, obj: object) -> int: ...
    def __enter__(self: Self) -> Self: ...
    async def __aenter__(self: Self) -> Self: ...
    def __ior__(self: Self, other: Self) -> Self: ...

class Fine:
    @typing_extensions.overload
    def __new__(cls, foo: int) -> FineSubclass: ...
    @overload
    def __new__(cls, *args: Any, **kwargs: Any) -> Fine: ...
    @abc.abstractmethod
    def __str__(self) -> str: ...
    @abc.abstractmethod
    def __repr__(self) -> str: ...
    def __eq__(self, other: Any, strange_extra_arg: list[str]) -> Any: ...
    def __ne__(self, *, kw_only_other: Any) -> bool: ...
    def __enter__(self) -> None: ...
    async def __aenter__(self) -> bool: ...

class FineSubclass(Fine): ...

class AlsoGood(str):
    def __str__(self) -> AlsoGood: ...
    def __repr__(self) -> AlsoGood: ...

class FineAndDandy:
    def __str__(self, weird_extra_arg) -> str: ...
    def __repr__(self, weird_extra_arg_with_default=...) -> str: ...

@final
class WillNotBeSubclassed:
    def __new__(cls, *args: Any, **kwargs: Any) -> WillNotBeSubclassed: ...
    def __enter__(self) -> WillNotBeSubclassed: ...
    async def __aenter__(self) -> WillNotBeSubclassed: ...

# we don't emit an error for these; out of scope for a linter
class InvalidButPluginDoesNotCrash:
    def __new__() -> InvalidButPluginDoesNotCrash: ...
    def __enter__() -> InvalidButPluginDoesNotCrash: ...
    async def __aenter__() -> InvalidButPluginDoesNotCrash: ...

class BadIterator1(Iterator[int]):
    def __iter__(self) -> Iterator[int]: ...  # Y034 "__iter__" methods in classes like "BadIterator1" usually return "self" at runtime. Consider using "_typeshed.Self" in "BadIterator1.__iter__", e.g. "def __iter__(self: Self) -> Self: ..."

class BadIterator2(typing.Iterator[int]):  # Y027 Use "collections.abc.Iterator[T]" instead of "typing.Iterator[T]" (PEP 585 syntax)
    def __iter__(self) -> Iterator[int]: ...  # Y034 "__iter__" methods in classes like "BadIterator2" usually return "self" at runtime. Consider using "_typeshed.Self" in "BadIterator2.__iter__", e.g. "def __iter__(self: Self) -> Self: ..."

class BadIterator3(typing.Iterator[int]):  # Y027 Use "collections.abc.Iterator[T]" instead of "typing.Iterator[T]" (PEP 585 syntax)
    def __iter__(self) -> collections.abc.Iterator[int]: ...  # Y034 "__iter__" methods in classes like "BadIterator3" usually return "self" at runtime. Consider using "_typeshed.Self" in "BadIterator3.__iter__", e.g. "def __iter__(self: Self) -> Self: ..."

class BadAsyncIterator(collections.abc.AsyncIterator[str]):
    def __aiter__(self) -> typing.AsyncIterator[str]: ...  # Y034 "__aiter__" methods in classes like "BadAsyncIterator" usually return "self" at runtime. Consider using "_typeshed.Self" in "BadAsyncIterator.__aiter__", e.g. "def __aiter__(self: Self) -> Self: ..."  # Y027 Use "collections.abc.AsyncIterator[T]" instead of "typing.AsyncIterator[T]" (PEP 585 syntax)

class Abstract(Iterator[str]):
    @abstractmethod
    def __iter__(self) -> Iterator[str]: ...
    @abstractmethod
    def __enter__(self) -> Abstract: ...
    @abstractmethod
    async def __aenter__(self) -> Abstract: ...

class GoodIterator(Iterator[str]):
    def __iter__(self: Self) -> Self: ...

class GoodAsyncIterator(AsyncIterator[int]):
    def __aiter__(self: Self) -> Self: ...

class DoesNotInheritFromIterator:
    def __iter__(self) -> DoesNotInheritFromIterator: ...

class Unannotated:
    def __new__(cls, *args, **kwargs): ...
    def __iter__(self): ...
    def __aiter__(self): ...
    async def __aenter__(self): ...
    def __repr__(self): ...
    def __str__(self): ...
    def __eq__(self): ...
    def __ne__(self): ...
    def __iadd__(self): ...
    def __ior__(self): ...

def __repr__(self) -> str: ...
def __str__(self) -> str: ...
def __eq__(self, other: Any) -> bool: ...
def __ne__(self, other: Any) -> bool: ...
def __imul__(self, other: Any) -> list[str]: ...
