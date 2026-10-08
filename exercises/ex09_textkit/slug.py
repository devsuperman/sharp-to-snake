"""URL slug helper."""


def slugify(text: str) -> str:
    """Turn ``text`` into a URL slug.

    Lower-case it, replace every run of non-alphanumeric characters with a single "-"
    (the ``re`` module helps), and strip leading/trailing dashes.

    Examples:
        slugify("Hello, World!")        -> "hello-world"
        slugify("  Python --- rocks ")  -> "python-rocks"
        slugify("!!!")                  -> ""
    """
    raise NotImplementedError
