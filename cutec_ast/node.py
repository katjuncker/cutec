from logging import warning

from cutec_bytecode.bytes import CutecBytes


class Node:
    def __init__(self):
        pass

    def __str__(self) -> str:
        return super().__str__()

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        warning('CuteC compile warning: ' + self.__class__.__name__ + ' does not implement add_bytes()')
        return bytecode