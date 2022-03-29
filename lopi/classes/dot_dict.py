import typing as t


class DotDict(dict):
    def __getattr__(self, key: str) -> object:
        return super().__getitem__(key)

    def __setattr__(self, key: str, value: object) -> None:
        super().__setattr__(key, value)

    def __delattr__(self, value: str) -> None:
        super().__delitem__(value)


class NestedDotDict(DotDict):
    def __init__(self, dct: t.Optional[dict] = None, **kwargs) -> None:
        if not dct:
            super().__init__(**kwargs)
        else:
            super().__init__({
                key: DotDict(value) if isinstance(value, dict) else value
                for key, value in dct.items()
            }, **kwargs)

    @staticmethod
    def _convert_to_dotdict(input: object) -> object:
        if input is None:
            return {}

        # Cast nested `dict`, `list` or `tuple` to `DotDict`.
        if isinstance(input, (list, tuple)):
            return [DotDict(d) for d in input]

        if isinstance(input, dict):
            return DotDict(input)

        return input

    def __setattr__(self, key: str, value: object) -> None:
        super().__setattr__(key, self._convert_to_dotdict(value))

    def __setitem__(self, key: str, value: object) -> None:
        super().__setitem__(key, self._convert_to_dotdict(value))
