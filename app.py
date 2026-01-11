import sys
import signal
import atexit
import logging
import threading
from infrastructure.config_manager import get_app_configuration, get_config_value
from flask import Flask
from infrastructure.log_manager import setup_logging
from infrastructure.file_manager import create_app_base_directory, get_file_path
from infrastructure.camera_manager import camera_manager
from api.face_recognition_api import face_recognition_api
from flask_cors import CORS
import pystray
from PIL import Image, ImageDraw
from infrastructure.mutex_manager import check_single_instance
import time
import webbrowser

# global ver for tray icon
tray_icon = None


def create_app():
    # setup configuration
    config = get_app_configuration()

    # setup directory
    create_app_base_directory(config)

    # setup logging
    setup_logging(config)

    # setup camera
    camera_manager.start()
    camera_health_check = camera_manager.health_check()
    logging.info(f"camera: {camera_health_check}")

    # setup flask
    app = Flask(__name__)
    app.register_blueprint(face_recognition_api)

    # handle CORS issues
    CORS(app)

    logging.info("finish create_app")

    return app


def run_flask(app, port):
    try:
        app.run(host="127.0.0.1", port=port, use_reloader=False)
    except Exception as e:
        logging.error(f"app.py => run_flask Error: {e}")
        shutdown_app()


def shutdown_app(*args):
    logging.info("app shutting down started")

    # stop camera
    camera_manager.stop()
    logging.info("camera stopped")

    # stop main thread
    global tray_icon
    if tray_icon:
        tray_icon.stop()


@atexit.register
def on_exit():
    camera_manager.stop()


if __name__ == "__main__":

    # use a mutex to prevent more than one instance of this app
    app_lock = check_single_instance()
    if not app_lock:
        print("application is already running. exiting now..")
        time.sleep(2)
        sys.exit(1)

    # handle CTRL+C
    signal.signal(signal.SIGINT, shutdown_app)
    signal.signal(signal.SIGTERM, shutdown_app)

    # create app configuration and paths, connect to camera, config logging and init flask app
    app = create_app()
    port = get_config_value("port", 8000)

    # run flask app on new thread
    flask_thread = threading.Thread(target=run_flask, args=(app, port), daemon=True)
    flask_thread.start()

    # create tray icon
    icon_path = get_file_path("ICON.ico")
    image = Image.open(icon_path)
    menu = pystray.Menu(
        pystray.MenuItem("זיהוי פנים פועל", lambda icon, item: None, enabled=False),
        pystray.MenuItem(
            "פתח דף ניהול", lambda icon, item: webbrowser.open("http://127.0.0.1:8000/")
        ),
        pystray.MenuItem("כיבוי", shutdown_app),
    )

    tray_icon = pystray.Icon("FaceRecognitionProject", image, "זיהוי פנים", menu)

    # run main thread using pystray icon
    tray_icon.run()

    # end of the app..
    sys.exit(0)
