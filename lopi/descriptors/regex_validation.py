import re
import typing as t

from .typed import StringTyped


class RegexDescriptor(StringTyped):
    def __init__(self, *args, pattern: t.Union[str, re.Pattern], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        self.pattern = pattern

    def __set__(self, instance: object, value: str) -> None:
        if not self.pattern.match(value):
            raise ValueError("String must match the regex pattern.")

        super().__set__(instance, value)
