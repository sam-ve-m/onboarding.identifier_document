# Jormungandr - Onboarding
from func.src.services.identifier_document import DocumentService
from tests.src.stubs import stub_payload_validated, stub_unique_id

# Third party
from pytest import fixture


@fixture(scope="function")
def document_service():
    service = DocumentService(
        payload_validated=stub_payload_validated, unique_id=stub_unique_id
    )
    return service
