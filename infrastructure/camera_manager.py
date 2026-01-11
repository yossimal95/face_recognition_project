import cv2
import threading
import time
import logging


class cameraManager:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self._lock = threading.Lock()
        self._latest_frame = None
        self._running = False
        self._thread = None
        self._last_update_time = 0
        self._start_time = 0

    def start(self):
        if self._running:
            return

        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            logging.error(f"could not open camera {self.camera_index}")
            return

        self._running = True
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    def _capture_loop(self):
        if self.cap is None:
            logging.error("camera is off")
            self.stop()
            return

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                with self._lock:
                    self._latest_frame = frame
                    self._last_update_time = time.time()
                    time.sleep(0.01)
                    if self.cap is None:
                        break
            else:
                logging.error("camera is off")
                break

    def get_latest_frame(self):
        with self._lock:
            return self._latest_frame.copy() if self._latest_frame is not None else None

    def health_check(self):
        now = time.time()

        # thread is alive
        is_thread_alive = self._thread is not None and self._thread.is_alive()

        # camera is open
        is_cap_open = self.cap is not None and self.cap.isOpened()

        # camera still working
        time_since_last_frame = (
            now - self._last_update_time if self._last_update_time > 0 else None
        )
        is_streaming = time_since_last_frame is not None and time_since_last_frame < 2.0

        # final status object
        status = {
            "is_running": self._running,
            "thread_alive": is_thread_alive,
            "device_opened": is_cap_open,
            "is_streaming": is_streaming,
            "time_since_last_frame_seconds": (
                round(time_since_last_frame, 2) if time_since_last_frame else "N/A"
            ),
        }

        # final status
        status["healthy"] = all(
            [self._running, is_thread_alive, is_cap_open, is_streaming]
        )

        return status

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        if self.cap:
            self.cap.release()
            self.cap = None
        self._latest_frame = None


camera_manager = cameraManager(camera_index=0)
