# Jormungandr - Onboarding
from ..enums.types import UserFileType, FileExtensionType


class DocumentModel:
    def __init__(self, unique_id: str, payload_validated: dict):
        self.unique_id = unique_id
        self.document_front = payload_validated.get("document_front")
        self.document_back = payload_validated.get("document_back")
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
        }
        return document_audit_template
