from typing import Protocol


class Notify(Protocol):
    def notify(self, *messages: str) -> None: ...


class PrintNotify(Notify):
    def notify(self, *message: str) -> None:
        print("\n".join(message))


def get_notify() -> Notify:
    return PrintNotify()
