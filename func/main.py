# Jormungandr - Onboarding
from src.domain.enums.code import InternalCode
from src.domain.exceptions.exceptions import (
    ErrorOnSendAuditLog,
    ErrorOnDecodeJwt,
    FileNotExists,
    InvalidOnboardingCurrentStep,
    OnboardingStepsStatusCodeNotOk,
    ErrorOnGetUniqueId,
)
from src.domain.response.model import ResponseModel
from src.domain.validators.validator import UserDocument
from src.services.identifier_document import DocumentService
from src.services.jwt import JwtService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


async def save_document() -> Response:
    raw_payload = request.json
    jwt = request.headers.get("x-thebes-answer")
    msg_error = "Unexpected error occurred"
    try:
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        payload_validated = UserDocument(**raw_payload).dict()
        document_service = DocumentService(
            unique_id=unique_id, payload_validated=payload_validated
        )
        await document_service.validate_current_onboarding_step(jwt=jwt)
        success = await document_service.save_user_document_file()
        response = ResponseModel(
            success=success,
            message="User identifier document saved successfully",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message=msg_error
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="User is not in document validation step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except FileNotExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND,
            message="Error on save document",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        Gladsheim.info(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid, extra or missing params",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
