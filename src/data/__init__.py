from enum import Enum, IntEnum


class ResultTypes(Enum):
    Time = 'Time'
    DNF = 'DNF'
    DNS = 'DNS'
    Extra = 'Extra'
    Empty = 'Empty'


class SetTypes(Enum):
    Train = 'train'
    Test = 'test'
    Validate = 'validate'


class ScoreDeckObjects(IntEnum):
    Event = 0
    Round = 1
    ID = 2
    ResultBox = 3
    MissingSignature = 4
    PlusTwo = 5
    Misc = 6


class CategoryObjects(IntEnum):
    E3x3 = 0
    E4x4 = 1
    E2x2 = 2
    E3x3OneHanded = 3
    EPyraminx = 4
    R1 = 5
    R2 = 6
    R3 = 7
    R4 = 8
    ID = 9
    MissingSignature = 10
    PlusTwo = 11
    Misc = 12
