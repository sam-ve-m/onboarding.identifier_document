# Standards
from re import match

# Third party
from pydantic import BaseModel, validator


class UserDocument(BaseModel):
    document_front: str
    document_back: str

    @validator("*", always=True, allow_reuse=True)
    def validate_content(cls, content) -> str:
        base_64_regex = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        if match(base_64_regex, content):
            return content
        raise ValueError("Base64 file content are invalid")
