class CustomFaceRecognitionException(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "An unspecified face_recognition error occurred"
        super().__init__(message)


class NoFacesDetected(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "No faces detected in front of the camera"
        super().__init__(message)


class InvalidBase64Image(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "Invalid Base64 image"
        super().__init__(message)


class NoFacesDetectedInBase64Image(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "No faces detected in Base64 image"
        super().__init__(message)


class MultipleFacesDetectedInBase64Image(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "Multiple faces detected in base64 image"
        super().__init__(message)


class CameraGeneralError(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "A general camera error occurred"
        super().__init__(message)


class MultipleFacesDetected(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "Multiple faces detected"
        super().__init__(message)


class FaceMismatch(CustomFaceRecognitionException):
    def __init__(self, message: str = None):
        if message is None:
            message = "Face mismatch detected"
        super().__init__(message)
