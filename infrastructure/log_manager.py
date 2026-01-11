import logging
import logging.handlers
import os


def setup_logging(config):
    app_drive = config.get("app_drive")
    app_base_directory_name = config.get("app_base_directory_name")
    log_directory = config.get("log_directory_name")
    log_path = f"{app_drive}/{app_base_directory_name}/{log_directory}"
    log_level_str = config.get("log_level", "INFO")

    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except PermissionError:
            print(f"ERROR: Cannot create log directory at {log_path}")
            return None

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.handlers.clear()

    # log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # create new log file every day
    log_file_path = os.path.join(log_path, "app_log.txt")

    try:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        file_handler.suffix = "%Y-%m-%d.txt"
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    except Exception as e:
        print(f"Failed to setup logging handlers: {e}")

    return logger
