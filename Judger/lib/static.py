from enum import IntEnum


class JUDGE_METHOD(IntEnum):
    Local = 0
    HDU = 1
    Codeforce = 2

class RESULT(IntEnum):
    ACCEPT = 0
    COMPILE_ERROR = 1
    TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    FORMAT_ERROR = 6
    WRONG_ANSWER = 7
    MULTI_ERROR = 8

    JUDGING = -1