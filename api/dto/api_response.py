from typing import Optional, Dict, Any
from flask import jsonify
from api.dto.error_codes import ErrorCodes


class ApiResponse:
    def __init__(
        self,
        success: bool = True,
        error: Optional[ErrorCodes] = None,
        body: Optional[Dict[str, Any]] = None,
    ):
        if success and error is not None:
            raise ValueError("ApiResponse cannot be successful and contain an error")

        if not success and error is None:
            raise ValueError("ApiResponse with success=False must contain an error")

        self.success = success
        self.error = error
        self.body = body or {}

    @classmethod
    def ok(cls, body: Optional[Dict[str, Any]] = None) -> "ApiResponse":
        return cls(success=True, body=body)

    @classmethod
    def fail(
        cls, error: ErrorCodes, body: Optional[Dict[str, Any]] = None
    ) -> "ApiResponse":
        return cls(success=False, error=error, body=body)

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "success": self.success,
            "body": self.body,
        }

        if not self.success and self.error:
            response.update(
                {
                    "error_code": self.error.code,
                    "description": self.error.description,
                    "he_description": self.error.he_description,
                    "message": self.error.display_message,
                }
            )

        return response

    def to_json(self):
        return jsonify(self.to_dict())
