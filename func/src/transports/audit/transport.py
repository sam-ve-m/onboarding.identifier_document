from ...domain.enums.types import QueueTypes
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.identifier_document.model import DocumentModel

from decouple import config
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, document_model: DocumentModel) -> bool:
        message = await document_model.get_user_document_audit_template()
        partition = QueueTypes.USER_DOCUMENT
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_USER_DOCUMENT_SCHEMA")
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            raise ErrorOnSendAuditLog()
        return True
