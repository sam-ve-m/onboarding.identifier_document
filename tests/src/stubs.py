# Jormungandr - Onboarding
from func.src.domain.validators.validator import UserDocument
from tests.src.image import image_b64


stub_content = {"Contents": {"test": "test"}}
stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_raw_payload = {
    "document_front": image_b64,
    "document_back": image_b64,
}
stub_payload_validated = UserDocument(**stub_raw_payload)
