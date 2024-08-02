from enum import IntEnum

class OcbErrorCode(IntEnum):
    NO_SERVICE = 62
    INSUFFICIENT_AMOUNT = 63
    OVERLIMIT_AMOUNT = 64
    UNNKNOWN_ERROR = 65
    TIMEOUT = 66
    OTP_FAILED = 67
    TRANSACTION_EXIST = 68
