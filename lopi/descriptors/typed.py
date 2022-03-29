import typing as t

from .base import _Descriptor


class _TypedDescriptor(_Descriptor):
    enforce_type = object  # Base type.

    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, self.enforce_type):
            raise TypeError(f"{self.name} must be of type {self.enforce_type}.")

        instance.__dict__[self.name] = value


class Typed(_TypedDescriptor):
    def __init__(self, enforce_type: type) -> None:
        self.enforce_type = enforce_type


class MultipleTyped(_TypedDescriptor):
    def __init__(self, *enforce_types: t.Tuple[type]) -> None:
        self.enforce_types = enforce_types

    def __set__(self, instance: object, value: object) -> None:
        super().__set__(instance, value)


# Descriptors for the specific types
class IntTyped(_TypedDescriptor):
    enforce_type = int


class FloatTyped(_TypedDescriptor):
    enforce_type = float

    # Auto-casting.
    def __set__(self, instance: object, value: t.Union[int, float]) -> None:
        if isinstance(value, int):
            value = float(value)

        super().__set__(instance, value)


class StringTyped(_TypedDescriptor):
    enforce_type = str


class BooleanTyped(_TypedDescriptor):
    enforce_type = bool


class ListTyped(_TypedDescriptor):
    enforce_type = list


class DictTyped(_TypedDescriptor):
    enforce_type = dict
