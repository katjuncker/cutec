from __future__ import annotations
from typing import TYPE_CHECKING

from logging import warning

if TYPE_CHECKING:
    from cutec_bytecode.packer import CutecBytes

class Node:
    def __init__(self):
        pass

    def __str__(self) -> str:
        return super().__str__()

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        warning('CuteC compile warning: ' + self.__class__.__name__ + ' does not implement add_bytes()')
        return bytecode