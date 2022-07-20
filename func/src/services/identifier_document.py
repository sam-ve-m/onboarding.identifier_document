# Jormungandr - Onboarding
from ..domain.exceptions import FileNotExists
from ..domain.identifier_document.model import DocumentModel
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit

# Standards
from base64 import b64decode
from io import SEEK_SET
from tempfile import TemporaryFile


class DocumentService:
    def __init__(self, unique_id, document_validated):
        self.document = DocumentModel(unique_id=unique_id, document_validated=document_validated)

    async def save_user_document_file(self) -> bool:
        temp_file_document_front = await DocumentService._resolve_content(self.document.document_front)
        temp_file_document_back = await DocumentService._resolve_content(self.document.document_back)
        await FileRepository.save_user_document_file(file_path=self.document.path_document_front, temp_file=temp_file_document_front)
        await FileRepository.save_user_document_file(file_path=self.document.path_document_back, temp_file=temp_file_document_back)
        await self._content_exists()
        await Audit.register_document_log(document_model=self.document)
        return True

    async def _content_exists(self):
        contents = [self.document.path_document_back, self.document.path_document_front]
        for content in contents:
            content_result = await FileRepository.list_contents(file_path=content)
            if content_result is None or "Contents" not in content_result:
                raise FileNotExists

    @staticmethod
    async def _resolve_content(document: str) -> TemporaryFile:
        decoded_document = b64decode(document)
        with TemporaryFile() as temp_file:
            temp_file.write(decoded_document)
            temp_file.seek(SEEK_SET)
            return temp_file
