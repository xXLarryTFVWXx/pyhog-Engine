from typing import Any


class State_Machine:
    def __init__(self):
        self.name: str = "default"
        self.sprites: list[object] = []
        self.objects: list[object] = []
        self._stack: list[dict] = []
    @property
    def stack(self) -> list[dict]:
        return self._stack
    
    @stack.setter
    def stack(self, value):
        self._stack[value['index']] = value['state'] if value['override'] else self._stack.append(value['state']) # type: ignore

state = State_Machine()