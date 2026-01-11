from enum import Enum


class ErrorCodes(Enum):
    # Format: NAME = (
    #   code,
    #  "description",
    #  "תיאור",
    #  "הודעה למשתמש"
    #   )
    # Http errors (700+)
    MISSING_REQUEST_BODY = (
        700,
        "No body was sent in the POST request",
        "לא נשלח גוף בקשה (body) בבקשת POST",
        "לא סופק תוכן לבקשה. אנא שלח את הנתונים הנדרשים ונסה שוב",
    )
    MISSING_BASE64_IMAGE = (
        701,
        "No Base64 image was provided in the request",
        "לא נשלחה תמונת Base64 בבקשה (מפתח: user_base64_image חסר)",
        "לא סופקה תמונת מקור. אנא נסה שוב או פנה לתמיכה",
    )
    # Face_recognition errors (100+)
    CAMERA_GENERAL_ERROR = (
        100,
        "A general camera error has occurred",
        "אירעה תקלה כללית במצלמה",
        "אירעה תקלה במצלמה. אנא פנה לתמיכה",
    )
    INVALID_BASE64_IMAGE = (
        101,
        "The provided image is not a valid or supported Base64 image",
        "התמונה שסופקה אינה תמונה תקינה בפורמט Base64 או שאינה נתמכת",
        "תמונת המקור לזיהוי אינה תקינה",
    )
    NO_FACE_DETECTED = (
        102,
        "No faces detected in front of the camera",
        "לא זוהו פנים בתמונה שהתקבלה מהמצלמה",
        "זיהוי פנים נכשל. נא ודא שפניך מופנות למצלמה ונסה שוב",
    )
    MULTIPLE_FACES_DETECTED = (
        103,
        "Multiple faces were detected in front of the camera",
        "זוהה יותר מאדם אחד מול המצלמה",
        "זוהה יותר מאדם אחד מול המצלמה. אנא ודא שרק אדם אחד נמצא מול המצלמה",
    )
    FACE_MISMATCH = (
        104,
        "The detected face does not match the expected person",
        "האדם שזוהה מול המצלמה אינו תואם לאדם עבורו סופקה תמונת מקור",
        "זיהוי נכשל: הפנים שנמצאו לא תואמות את הפרטים שסופקו. אנא ודא שאתה מול המצלמה ונסה שוב",
    )
    NO_FACE_DETECTED_IN_BASE64_IMAGE = (
        106,
        "No face was detected in the provided Base64 image",
        "לא זוהו פנים בתמונה שסופקה כ־Base64",
        "לא זוהו פנים בתמונת המקור. אנא נסה שוב נסה שוב או פנה לתמיכה",
    )
    MULTIPLE_FACES_DETECTED_IN_BASE64_IMAGE = (
        107,
        "Multiple faces were detected in the base64 image",
        "זוהה יותר מאדם אחד בתמונת המקור",
        "זוהה יותר מאדם אחד בתמונת המקור, אנא נסה שוב או פנה לתמיכה",
    )

    # Sys errors (900+)
    GENERAL_ERROR = (
        900,
        "A general error has occurred",
        "אירעה תקלה כללית במערכת",
        "אירעה שגיאה כללית. אנא נסה שוב או פנה לתמיכה",
    )

    @property
    def code(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @property
    def he_description(self):
        return self.value[2]

    @property
    def display_message(self):
        return f"{self.value[3]} - קוד שגיאה: {self.value[0]}"
