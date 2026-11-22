from enum import StrEnum

class BaseType (StrEnum):
    Primitive = 'p'
    Action = 'a'
    Thing = 't'
    Placeholder = '-'