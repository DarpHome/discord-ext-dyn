class _Replacer(dict):
    def __missing__(self, key: str) -> str:
        return rf"(?P<{key}>\w+)"


def format_as_regex(format: str) -> str:
    return format.format_map(_Replacer())
