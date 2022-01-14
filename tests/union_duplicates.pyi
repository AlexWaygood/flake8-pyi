from typing import Union

def f1_pipe(x: int | str) -> None:  # no error
    ...
def f2_pipe(x: int | int) -> None:  # Y016
    ...
def f3_pipe(x: None | int | int) -> None:  # Y016
    ...
def f4_pipe(x: int | None | int) -> None:  # Y016
    ...
def f5_pipe(x: int | int | None) -> None:  # Y016
    ...

def f1_union(x: Union[int, str]) -> None:  # no error
    ...
def f2_union(x: Union[int, int]) -> None:  # Y016
    ...
def f3_union(x: Union[None, int, int]) -> None:  # Y016
    ...
def f4_union(x: Union[int, None, int]) -> None:  # Y016
    ...
def f5_union(x: Union[int, int, None]) -> None:  # Y016
    ...