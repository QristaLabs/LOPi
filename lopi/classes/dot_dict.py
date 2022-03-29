import typing as t


class DotDict(dict):
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

    # Overrides
    def __setattr__(self, key: str, value: object) -> None:
        super().__setattr__(key, self._convert_to_dotdict(value))

    def __setitem__(self, key: str, value: object) -> None:
        super().__setitem__(key, self._convert_to_dotdict(value))

    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__  # type: ignore
