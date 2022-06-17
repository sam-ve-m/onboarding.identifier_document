# Standards
from re import match

# Third party
from pydantic import BaseModel, constr, validator


class UserDocument(BaseModel):
    document_front: constr(min_length=258)
    document_back: constr(min_length=258)

    @validator("content", always=True, allow_reuse=True)
    def validate_content(cls, content):
        base_64_regex = r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$'
        if match(base_64_regex, content):
            return content
        raise ValueError("Base64 file content are invalid")
