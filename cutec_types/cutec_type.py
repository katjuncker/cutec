from enum import StrEnum


class CutecType (StrEnum):
    Str = 's'
    Int = 'i'
    Char = 'c'
    Dbl = 'd'
    Bool = 'b'
    Stack = 'x'
    Obj = 'o'
    Action = 'a'
    Thing = 't'