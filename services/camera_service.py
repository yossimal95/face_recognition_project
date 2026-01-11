from infrastructure.camera_manager import camera_manager
from infrastructure.file_manager import get_file_path
from utils.base64_util import convert_images_to_base64
import time
import face_recognition
import cv2
import base64
import numpy as np
from infrastructure.custom_face_recognition_exceptions import (
    InvalidBase64Image,
    NoFacesDetected,
    MultipleFacesDetected,
    FaceMismatch,
    NoFacesDetectedInBase64Image,
    MultipleFacesDetectedInBase64Image,
)


# region public methods
# get camera health status
def get_camera_health_check():
    camera_health_check = camera_manager.health_check()
    return camera_health_check


# generate frames for vido feed
def generate_frames():
    xml_path = get_file_path("static/haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(xml_path)

    # Track frames to skip detection
    process_this_frame = 0
    cached_faces = []

    while camera_manager._running:
        frame = camera_manager.get_latest_frame()
        if frame is None:
            continue

        # Only run detection every 4th frame
        if process_this_frame % 4 == 0:
            # 1. Resize for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            frame_gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

            cached_faces = face_cascade.detectMultiScale(
                frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

        # Draw the rectangles (adjusting coordinates back up by 4x)
        for x, y, w, h in cached_faces:
            cv2.rectangle(
                frame, (x * 4, y * 4), ((x + w) * 4, (y + h) * 4), (255, 0, 0), 2
            )

        process_this_frame += 1

        # Encode and Yield
        ret, buffer = cv2.imencode(".jpg", frame)
        if ret:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

        if process_this_frame > 1000:
            process_this_frame = 0
        # Sync with actual camera FPS (e.g., 30fps = ~0.03s)
        time.sleep(0.03)


# compare base64 image with current user face
def compare_user_image_with_camera_current_user(user_base64_image: str):
    if "," in user_base64_image:
        user_base64_image = user_base64_image.split(",")[1]

    encoded_data = base64.b64decode(user_base64_image)
    nparr = np.frombuffer(encoded_data, np.uint8)

    # Decode to BGR (OpenCV default)
    stored_img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if stored_img_bgr is None:
        raise InvalidBase64Image()

    # IMPORTANT: Convert BGR to RGB for face_recognition
    stored_img_rgb = cv2.cvtColor(stored_img_bgr, cv2.COLOR_BGR2RGB)

    # Get the encoding
    stored_encodings = face_recognition.face_encodings(stored_img_rgb)
    if not stored_encodings:
        raise NoFacesDetectedInBase64Image()

    if len(stored_encodings) > 1:
        raise MultipleFacesDetectedInBase64Image()

    stored_encoding = stored_encodings[0]

    user_images = get_current_user_images()

    match_count = 0

    for img in user_images:
        # Note: Ensure get_current_user_images() returns RGB frames
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        captured_encs = face_recognition.face_encodings(img)
        if not captured_encs:
            raise NoFacesDetected()

        results = face_recognition.compare_faces(
            [stored_encoding], captured_encs[0], tolerance=0.6
        )

        if results[0]:
            match_count += 1
        else:
            raise FaceMismatch()

    return {
        "face_recognition_success": True,
        "images": convert_images_to_base64(user_images),
    }


# endregion


# region private methods
def get_current_user_images():
    images = []
    encodings = []
    padding = 80
    required_samples = 5
    max_attempts = 15

    for _ in range(max_attempts):
        if len(encodings) >= required_samples:
            break

        frame = camera_manager.get_latest_frame()
        if frame is None:
            continue

        # Convert BGR (OpenCV default) to RGB (face_recognition requirement)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(frame, model="hog")

        if len(face_locations) == 0:
            continue
        elif len(face_locations) > 1:
            raise MultipleFacesDetected()

        current_encoding = face_recognition.face_encodings(frame, face_locations)[0]

        if encodings:
            match = face_recognition.compare_faces(
                [encodings[0]], current_encoding, tolerance=0.6
            )
            if not match[0]:
                raise MultipleFacesDetected()

        top, right, bottom, left = face_locations[0]
        top_p = max(0, top - padding)
        bottom_p = min(frame.shape[0], bottom + padding)
        left_p = max(0, left - padding)
        right_p = min(frame.shape[1], right + padding)

        cropped_face = frame[top_p:bottom_p, left_p:right_p]

        images.append(cropped_face)
        encodings.append(current_encoding)

        time.sleep(0.2)

    if len(images) < required_samples:
        raise NoFacesDetected()

    return images


# endregion
