# face_recognition_project installation guide

### Install Miniconda here: https://www.anaconda.com/download/success

### (!important: *Miniconda - not *Anaconda)

## Then run:

conda create -n face_recognition_project python=3.10 -y

conda activate face_recognition_project

conda install -c conda-forge dlib -y

pip install "numpy<2" "opencv-python<4.10" face_recognition pyinstaller flask flask-cors pystray pillow

# Pyinstaller build command:

```
pyinstaller --noconsole --onefile --name="FaceRecognitionApp" --collect-all face_recognition --icon="ICON.ico" --add-data "ICON.ico;." --collect-all face_recognition_models --add-data "static/haarcascade_frontalface_default.xml;static" --collect-all dlib app.py
```
