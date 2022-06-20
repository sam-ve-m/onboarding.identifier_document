# Standards
from enum import IntEnum

from strenum import StrEnum


class QueueTypes(IntEnum):
    USER_DOCUMENT = 7

    def __repr__(self):
        return self.value


class UserFileType(StrEnum):
    DOCUMENT_FRONT = "document_front"
    DOCUMENT_BACK = "document_back"

    def __repr__(self):
        return self.value


class FileExtensionType(StrEnum):
    DOCUMENT_EXTENSION = ".jpg"

    def __repr__(self):
        return self.value
