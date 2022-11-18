from base64 import b64decode
from io import SEEK_SET
from tempfile import TemporaryFile

from ..domain.enums.types import UserOnboardingStep
from ..domain.exceptions.exceptions import FileNotExists, InvalidOnboardingCurrentStep
from ..domain.identifier_document.model import DocumentModel
from ..domain.validators.validator import UserDocument
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit
from ..transports.onboarding_steps.transport import OnboardingSteps


class DocumentService:
    def __init__(self, unique_id: str, payload_validated: UserDocument):
        self.document = DocumentModel(
            unique_id=unique_id, payload_validated=payload_validated
        )

    @staticmethod
    async def validate_current_onboarding_step(jwt: str) -> bool:
        user_current_step_br = await OnboardingSteps.get_user_current_step_br(jwt=jwt)
        if user_current_step_br == UserOnboardingStep.FINISHED_BR:
            user_current_step_us = await OnboardingSteps.get_user_current_step_us(
                jwt=jwt
            )
            if not user_current_step_us == UserOnboardingStep.IDENTIFIER_DOCUMENT_US:
                raise InvalidOnboardingCurrentStep
        elif not user_current_step_br == UserOnboardingStep.IDENTIFIER_DOCUMENT_BR:
            raise InvalidOnboardingCurrentStep
        return True

    async def save_user_document_file(self) -> bool:

        temp_file_document_front = await DocumentService._resolve_content(
            self.document.document_front
        )
        temp_file_document_back = await DocumentService._resolve_content(
            self.document.document_back
        )
        await Audit.record_message_log(document_model=self.document)
        await FileRepository.save_user_document_file(
            file_path=self.document.path_document_front,
            temp_file=temp_file_document_front,
        )
        await FileRepository.save_user_document_file(
            file_path=self.document.path_document_back,
            temp_file=temp_file_document_back,
        )
        await self._content_exists()
        return True

    async def _content_exists(self) -> bool:
        contents = [self.document.path_document_back, self.document.path_document_front]
        for content in contents:
            content_result = await FileRepository.list_contents(file_path=content)
            if content_result is None or "Contents" not in content_result:
                raise FileNotExists
        return True

    @staticmethod
    async def _resolve_content(document: str) -> TemporaryFile:
        decoded_document = b64decode(document)
        temp_file = TemporaryFile()
        temp_file.write(decoded_document)
        temp_file.seek(SEEK_SET)
        return temp_file
