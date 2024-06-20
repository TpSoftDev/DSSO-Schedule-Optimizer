from enum import Enum

class URLs(Enum):
    GET_CLASS_SCHEDULE = ""
    GET_CLASS_SCHEDULE_TEST = "https://081c4a2a-6343-49a2-9c38-1835834d8a00.mock.pstmn.io/Classes" #Newest URL
    AUTHENTICATE = "https://test.tmwork.net/2023.1/api/ops/auth"

    GET_CLASS_SCHEDULE_TEST_FIRST = "https://73e3a015-c6d6-4d11-b52d-7bf2de6f3541.mock.pstmn.io/Classes/First"

    GET_CLASS_SCHEDULE_TEST_SECOND = "https://d6c44a80-fe54-4811-9c63-498d87c948a5.mock.pstmn.io/Classes"

    GET_CLASS_SCHEDULE_TEST_THIRD = "https://73e3a015-c6d6-4d11-b52d-7bf2de6f3541.mock.pstmn.io/Classes/Third"

    GET_CLASS_SCHEDULE_TEST_FOURTH = "https://73e3a015-c6d6-4d11-b52d-7bf2de6f3541.mock.pstmn.io/Classes/Fourth"
