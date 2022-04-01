import typing as t


class FreezeClassAttributesMeta(type):
    """Metaclass to freeze the class attributes."""
    def __new__(
        cls,
        name: str,
        bases: t.Tuple[type, ...],
        attrs: t.Dict[str, t.Any],
        *,
        frozen_attributes: t.Optional[t.Union[str, t.Iterable[str]]] = None,
        allow_new_attrs: bool = False
    ):
        # Set the attributes property as `__frozen_attributes__`.
        attrs["__frozen_attributes__"] = (frozen_attributes,) \
            if isinstance(frozen_attributes, str) \
            else frozen_attributes

        # Allow new attributes to be added to the class.
        attrs["__allow_new_attrs__"] = allow_new_attrs

        return super().__new__(cls, name, bases, attrs)

    def __setattr__(cls, key: str, value: t.Any) -> None:
        if key in cls.__dict__:
            frozen_methods = cls.__dict__.get("__frozen_attributes__", None)

            # If frozen methods is None, or empty tuple, then disable setting all attributes.
            if frozen_methods is None or not frozen_methods:
                raise TypeError(f"`{key}` attribute is immutable.")

            # Else, Disable setting value of the specific attributes.
            if key not in frozen_methods:
                super().__setattr__(key, value)
            else:
                raise TypeError(f"`{key}` attribute is immutable.")
        else:
            if not cls.__dict__.get("__allow_new_attrs__", False):
                raise TypeError(f"`{key}` attribute is immutable.")

            super().__setattr__(key, value)
