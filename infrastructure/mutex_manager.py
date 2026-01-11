import ctypes

ERROR_ALREADY_EXISTS = 183


def check_single_instance(app_name="faceRecognitionProject"):

    lock_name = "Local\\" + app_name

    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, lock_name)

    last_error = ctypes.windll.kernel32.GetLastError()

    if last_error == ERROR_ALREADY_EXISTS:
        return None

    return mutex
