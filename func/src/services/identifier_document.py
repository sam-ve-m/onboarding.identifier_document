# Jormungandr - Onboarding
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit
from ..domain.identifier_document.model import DocumentModel

# Standards
from base64 import b64decode
from io import SEEK_SET
from tempfile import TemporaryFile


class DocumentService:
    def __init__(self, unique_id, document_validated):
        self.unique_id = unique_id
        self.document = DocumentModel(unique_id=unique_id, document_validated=document_validated)

    def save_user_document_file(self):
        temp_file_document_front = DocumentService._resolve_content(self.document.document_front)
        temp_file_document_back = DocumentService._resolve_content(self.document.document_back)
        await FileRepository.save_user_document_file(file_path=self.document.path_document_front, temp_file=temp_file_document_front)
        await FileRepository.save_user_document_file(file_path=self.document.path_document_back, temp_file=temp_file_document_back)
        await Audit.register_document_log(document_model=self.document)
        return True

    @staticmethod
    async def _resolve_content(document: str) -> TemporaryFile:
        decoded_document = b64decode(document)
        with TemporaryFile() as temp_file:
            temp_file.write(decoded_document)
            temp_file.seek(SEEK_SET)
            return temp_file
