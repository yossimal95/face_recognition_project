import cv2
import base64


def convert_images_to_base64(images_list):
    """
    Converts a list of RGB numpy arrays to a list of Base64 strings.
    """
    base64_strings = []

    for img_rgb in images_list:
        # 1. Convert back to BGR because cv2.imencode expects BGR
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # 2. Encode the image to a JPEG buffer
        # We use a quality of 90 to keep the file size small but clear
        success, buffer = cv2.imencode(".jpg", img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])

        if success:
            # 3. Convert bytes to base64 string
            b64_str = base64.b64encode(buffer).decode("utf-8")

            # 4. Add the Data URI prefix so the frontend <img> tag can use it directly
            full_b64 = f"data:image/jpeg;base64,{b64_str}"
            base64_strings.append(full_b64)

    return base64_strings
