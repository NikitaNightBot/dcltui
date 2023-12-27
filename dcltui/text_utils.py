from sys import stdout


def write(
    text: str,
    flush: bool = False,
    w=stdout.write,
    f=stdout.flush,  # local names faster lookup
) -> None:
    w(text)
    if flush:
        f()


def right_pad(text: str, size: int) -> str:
    return (text + (" " * (size - len(text))))[-size:]
