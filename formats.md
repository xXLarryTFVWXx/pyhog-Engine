# Format file
This file contains the formats for each object and states.
Each state is a python object

## State format
The state dictionary contains various states.
``` python
{
    "state name": str,
    "state type": str,
    "level wrapping: list[int],
    "characters": list[Character]
    "monitors": list[item]
}
```