# Standards
from enum import IntEnum

# Third party
from strenum import StrEnum


class QueueTypes(IntEnum):
    USER_DOCUMENT = 7

    def __repr__(self):
        return self.value


class UserFileType(StrEnum):
    DOCUMENT_FRONT = "document_front"
    DOCUMENT_BACK = "document_back"


class FileExtensionType(StrEnum):
    DOCUMENT_EXTENSION = ".jpg"


class UserOnboardingStep(StrEnum):
    IDENTIFIER_DOCUMENT = "document_validator"
