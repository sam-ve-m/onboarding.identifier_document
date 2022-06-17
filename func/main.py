# Jormungandr - Onboarding
from src.domain.enums.code import InternalCode
from src.domain.exceptions import ErrorOnSendAuditLog, ErrorOnDecodeJwt, ErrorOnUpdateUser, UserUniqueIdNotExists, FileNotExists
from src.domain.response.model import ResponseModel
from src.domain.validator import UserDocument
from src.services.identifier_document import DocumentService
from src.services.jwt import JwtService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request


async def save_document():
    raw_document = request.json
    jwt = request.headers.get("x-thebes-answer")
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
    msg_error = "Unexpected error occurred"
    try:
        document_validated = UserDocument(**raw_document).dict()
        document_service = DocumentService(unique_id=unique_id, document_validated=document_validated)
        success = await document_service.save_user_document_file()
        response = ResponseModel(
            success=success,
            message="User identifier document saved successfully",
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message=msg_error
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except FileNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnUpdateUser as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError:
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid base64 string"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
