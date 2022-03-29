import typing as t


class _Descriptor:
    def __set_name__(self, owner: t.Type[object], name: str) -> None:
        self.name = name

    def __get__(self, instance: t.Optional[object], owner: t.Type[object]) -> object:
        if instance is None:
            return self

        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: object) -> None:
        instance.__dict__[self.name] = value

    def __delete__(self, instance: object) -> None:
        del instance.__dict__[self.name]
