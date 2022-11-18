from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response

from func.src.transports.device_info.transport import DeviceSecurity
from src.domain.enums.code import InternalCode
from src.domain.exceptions.exceptions import (
    ErrorOnSendAuditLog,
    ErrorOnDecodeJwt,
    FileNotExists,
    InvalidOnboardingCurrentStep,
    OnboardingStepsStatusCodeNotOk,
    ErrorOnGetUniqueId,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from src.domain.response.model import ResponseModel
from src.domain.validators.validator import UserDocument
from src.services.identifier_document import DocumentService
from src.services.jwt import JwtService


async def save_document() -> Response:
    msg_error = "Unexpected error occurred"
    try:
        raw_payload = request.json
        x_thebes_answer = request.headers.get("x-thebes-answer")
        x_device_info = request.headers.get("x-device-info")

        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=x_thebes_answer)
        device_info = await DeviceSecurity.get_device_info(x_device_info)

        payload_validated = UserDocument(**raw_payload)
        document_service = DocumentService(
            unique_id=unique_id,
            payload_validated=payload_validated,
            device_info=device_info,
        )
        await document_service.validate_current_onboarding_step(jwt=x_thebes_answer)
        success = await document_service.save_user_document_file()
        response = ResponseModel(
            success=success,
            message="User identifier document saved successfully",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="Unauthorized token"
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
            message="User is not in correct step",
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

    except DeviceInfoRequestFailed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
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
