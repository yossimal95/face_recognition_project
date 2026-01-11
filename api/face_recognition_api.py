from flask import Blueprint, Response, request, jsonify, abort, make_response
from services.camera_service import (
    generate_frames,
    get_camera_health_check,
    compare_user_image_with_camera_current_user,
)
from infrastructure.custom_face_recognition_exceptions import (
    InvalidBase64Image,
    NoFacesDetected,
    MultipleFacesDetected,
    FaceMismatch,
    NoFacesDetectedInBase64Image,
    MultipleFacesDetectedInBase64Image,
)
from static.config_html import config_html
from api.dto.api_response import ApiResponse
from werkzeug.exceptions import HTTPException
from api.dto.error_codes import ErrorCodes
import logging

face_recognition_api = Blueprint("face_recognition_api", __name__)


# config page
@face_recognition_api.route("/", methods=["GET"])
def index():
    try:
        return config_html
    except Exception as e:
        logging.error(f"face_recognition_api => index Error: {e}", exc_info=True)
        return make_response(ApiResponse.fail(ErrorCodes.GENERAL_ERROR).to_json(), 500)


# get camera health status
@face_recognition_api.route("/get_camera_status", methods=["GET"])
def get_camera_status():
    try:
        camera_health_check = get_camera_health_check()
        if not camera_health_check["healthy"]:
            logging.error(
                f"face_recognition_api => get_camera_status Error => camera error: {camera_health_check}",
                exc_info=True,
            )
            return make_response(
                ApiResponse.fail(
                    ErrorCodes.CAMERA_GENERAL_ERROR, camera_health_check
                ).to_json(),
                500,
            )

        return ApiResponse.ok(camera_health_check).to_json()
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"face_recognition_api => get_camera_status Error: {e}", exc_info=True)
        return make_response(ApiResponse.fail(ErrorCodes.GENERAL_ERROR).to_json(), 500)


# get video from camera
@face_recognition_api.route("/video_feed", methods=["GET"])
def video_feed():
    try:
        return Response(
            generate_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )
    except Exception as e:
        logging.error(f"face_recognition_api => video_feed Error: {e}", exc_info=True)
        return make_response(ApiResponse.fail(ErrorCodes.GENERAL_ERROR).to_json(), 500)


# compare base46 image face with current user face
@face_recognition_api.route("/validate_current_user_with_image", methods=["POST"])
def validate_current_user_with_image():
    face_recognition_error_http_code = 200
    try:
        body = request.get_json()
        if not body:
            logging.error(
                f"face_recognition_api => validate_current_user_with_image MISSING_REQUEST_BODY Error: {e}",
                exc_info=True,
            )
            return make_response(
                ApiResponse.fail(ErrorCodes.MISSING_REQUEST_BODY).to_json(),
                face_recognition_error_http_code,
            )

        user_base64_image = body.get("user_base64_image")
        if user_base64_image is None:
            logging.error(
                f"face_recognition_api => validate_current_user_with_image MISSING_BASE64_IMAGE Error: {e}",
                exc_info=True,
            )
            return make_response(
                ApiResponse.fail(ErrorCodes.MISSING_BASE64_IMAGE).to_json(),
                face_recognition_error_http_code,
            )

        camera_health_check = get_camera_health_check()
        if not camera_health_check["healthy"]:
            logging.error(
                f"face_recognition_api => validate_current_user_with_image Error => camera error: {camera_health_check}",
                exc_info=True,
            )
            return make_response(
                ApiResponse.fail(
                    ErrorCodes.CAMERA_GENERAL_ERROR, camera_health_check
                ).to_json(),
                face_recognition_error_http_code,
            )

        result = compare_user_image_with_camera_current_user(user_base64_image)

        return ApiResponse().ok(body=result).to_json()
    except InvalidBase64Image as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image => InvalidBase64Image Error: {e}",
            exc_info=True,
        )
        return (
            make_response(ApiResponse.fail(ErrorCodes.INVALID_BASE64_IMAGE).to_json()),
            face_recognition_error_http_code,
        )
    except MultipleFacesDetectedInBase64Image as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image => MultipleFacesDetectedInBase64Image Error: {e}",
            exc_info=True,
        )
        return (
            make_response(
                ApiResponse.fail(
                    ErrorCodes.MULTIPLE_FACES_DETECTED_IN_BASE64_IMAGE
                ).to_json()
            ),
            face_recognition_error_http_code,
        )
    except NoFacesDetected as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image => NoFacesDetected Error: {e}",
            exc_info=True,
        )
        return make_response(
            ApiResponse.fail(ErrorCodes.NO_FACE_DETECTED).to_json(),
            face_recognition_error_http_code,
        )
    except MultipleFacesDetected as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image => MultipleFacesDetected Error: {e}",
            exc_info=True,
        )
        return make_response(
            ApiResponse.fail(ErrorCodes.MULTIPLE_FACES_DETECTED).to_json(),
            face_recognition_error_http_code,
        )
    except FaceMismatch as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image => FaceMismatch Error: {e}",
            exc_info=True,
        )
        return make_response(
            ApiResponse.fail(ErrorCodes.FACE_MISMATCH).to_json(),
            face_recognition_error_http_code,
        )
    except NoFacesDetectedInBase64Image as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image => NoFacesDetectedInBase64Image Error: {e}",
            exc_info=True,
        )
        return make_response(
            ApiResponse.fail(ErrorCodes.NO_FACE_DETECTED_IN_BASE64_IMAGE).to_json(),
            face_recognition_error_http_code,
        )
    # default exception
    except Exception as e:
        logging.error(
            f"face_recognition_api => validate_current_user_with_image Error: {e}",
            exc_info=True,
        )
        return make_response(ApiResponse.fail(ErrorCodes.GENERAL_ERROR).to_json(), 500)
