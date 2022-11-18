from func.src.services.identifier_document import DocumentService
from tests.src.services.identifier_document.stubs import (
    stub_payload_validated,
    stub_unique_id,
    stub_device_info,
)

from pytest import fixture


@fixture(scope="function")
def document_service():
    service = DocumentService(
        payload_validated=stub_payload_validated,
        unique_id=stub_unique_id,
        device_info=stub_device_info,
    )
    return service
