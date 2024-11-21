import functools, pygame
from . import events
CLOCK = pygame.time.Clock()

timers = []

@functools.lru_cache(maxsize=1)
def get_clock() -> pygame.time.Clock:
    return CLOCK


def tick(target_framerate) -> None:
    CLOCK.tick(target_framerate)

@functools.lru_cache(maxsize=1)
def get_delta_time():
    return CLOCK.get_time() / 1000

def create_timer(event:pygame.event.Event, delay=100, occurances=1):
    events.verify_event(event)
    pygame.time.set_timer(event, delay, occurances)
    timers.append(event)

def delete_timer(event:pygame.event.Event):
    events.verify_event(event)
    assert event in timers, f"There is no timer associated with the event {pygame.event.event_name(event.type)}"
    pygame.time.set_timer(event, 0)


__all__ = [
    "get_clock",
    "tick",
    "create_timer",
    "delete_timer"
]