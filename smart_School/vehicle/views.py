

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
from django.views.decorators.http import require_GET
from app_resources.models import Cameras
from imutils.video import VideoStream
from app_resources.utils import cameras
import cv2
import numpy as np
import torch

from detect import detect
from models.experimental import attempt_load
from src.char_classification.model import CNN_Model
from utils_LP import character_recog_CNN, crop_n_rotate_LP
import sys
# Load character recognition model
CHAR_CLASSIFICATION_WEIGHTS = './weight.h5'
model_char = CNN_Model(trainable=False).model
model_char.load_weights(CHAR_CLASSIFICATION_WEIGHTS)

# Load license plate detection model
LP_weights = './LP_detect_yolov7_500img.pt'
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model_LP = attempt_load(LP_weights, map_location=device)




def open_camera(request, id):
    camera = Cameras.objects.filter(id=id).first()
    return render(request, 'vehicle/detect_vehicle.html', context={
        "cameras": Cameras.objects.all(),
        "camera": camera,
        # 'reasons':Reasons.objects.filter(when='الدخول' if camera.camera_type=='indoor' else 'الخروج')
    })
    

camera=None
@gzip.gzip_page
@require_GET
def verticle_camera(request, camera_id):
    cam = Cameras.objects.filter(id=camera_id).first()
    connection_string = cam.connection_string
    if connection_string == '0':
        connection_string = 0
    if connection_string == '1':
        connection_string = 1
    global camera
    if camera is not None:
        camera.stream.stop()
        camera=None
    camera = VideoStream(connection_string)
    camera.start()
    cameras.append({"id":cam.id, "camera": camera})
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
    
def generate():
    while True:
        frame = camera.read()
        if camera is None:
            break
        if frame is None:
            continue
        red, LP_detected_img, result = detect(model_LP, frame, device, imgsz=640)
        
        _, jpeg = cv2.imencode('.jpg', LP_detected_img)

        data = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
        