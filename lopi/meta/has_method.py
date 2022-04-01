import typing as t


class HasMethodMeta(type):
    def __new__(
        cls,
        name: str,
        bases: t.Tuple[type, ...],
        attrs: t.Dict[str, t.Any],
        *,
        method_names: t.Union[str, t.Iterable[str]]
    ):
        # Convert to tuple if not already.
        if isinstance(method_names, str):
            method_names = (method_names,)

        # Ensure all methods exist
        for method in method_names:
            if method not in attrs:
                raise TypeError(f"{name} does not have method `{method}`.")

            # If the method is a classmethod or staticmethod, ignore.
            # This is because classmethod and staticmethod objects are descriptors.
            if isinstance(attrs[method], (classmethod, staticmethod)):
                continue

            # If the method is not callable, raise error.
            if not callable(attrs[method]):
                raise TypeError(f"`{name}.{method}` is not callable.")

        # Return the class
        return super().__new__(cls, name, bases, attrs)
