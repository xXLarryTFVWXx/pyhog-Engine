from typing import Any
import json
import pygame

class Machine:
    def __init__(self):
        self.states: dict[str, dict[str, Any]] = {}
        self.current_state: dict[str, dict[str, Any]] = {"empty": {"name": "empty"}}
    def change_state(self, state_name: str):
        if state_name.lower() == "quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            self.save_to_file()
            return
        self.current_state = self.states[state_name]
    def get_current_state(self):
        return self.current_state
    def save_to_file(self):
        with open("state_machine.json", mode="w") as file:
            json.dump(self.current_state, file)

State_machine = Machine()