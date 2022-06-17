# Jormungandr - Onboarding
from func.src.services.identifier_document import DocumentService
from tests.src.stubs import stub_document_validated, stub_unique_id

# Third party
from pytest import fixture


@fixture(scope='function')
def document_service():
    service = DocumentService(document_validated=stub_document_validated, unique_id=stub_unique_id)
    return service
