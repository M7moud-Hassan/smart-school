
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
from django.views.decorators.http import require_GET
from app_resources.models import Cameras
from imutils.video import VideoStream
from app_resources.utils import cameras

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
        _, jpeg = cv2.imencode('.jpg', frame)
        data = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
        