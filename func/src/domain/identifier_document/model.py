from ..models.device_info import DeviceInfo
from ...domain.validators.validator import UserDocument
from ..enums.types import UserFileType, FileExtensionType


class DocumentModel:
    def __init__(
        self, unique_id: str, payload_validated: UserDocument, device_info: DeviceInfo
    ):
        self.unique_id = unique_id
        self.device_info = device_info
        self.document_front = payload_validated.document_front
        self.document_back = payload_validated.document_back
        self.path_document_front = (
            f"{self.unique_id}/{UserFileType.DOCUMENT_FRONT}/{UserFileType.DOCUMENT_FRONT}"
            f"{FileExtensionType.DOCUMENT_EXTENSION}"
        )
        self.path_document_back = (
            f"{self.unique_id}/{UserFileType.DOCUMENT_BACK}/{UserFileType.DOCUMENT_BACK}"
            f"{FileExtensionType.DOCUMENT_EXTENSION}"
        )

    async def get_user_document_audit_template(self) -> dict:
        document_audit_template = {
            "unique_id": self.unique_id,
            "path_document_front": self.path_document_front,
            "path_document_back": self.path_document_back,
            "device_info": self.device_info.device_info,
            "device_id": self.device_info.device_id,
        }
        return document_audit_template
