import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
from django.views.decorators.http import require_GET
from app_resources.models import *
from app_resources.utils import cameras, detect_person,detect_unknown

from deepface import DeepFace
import cv2
import pickle
import numpy as np
import os
from django.conf import settings
from deepface.commons import functions, realtime, distance as dst
#from retinaface import RetinaFace

def all_cameras(request):
    camears_lisy = Cameras.objects.all()
    return render(request, 'livefeed/all.html', context={
        "title": "View Cameras",
        "sub_title": "All",
        "cameras": camears_lisy
    })


def open_camera(request, id):
    camera = Cameras.objects.filter(id=id).first()
    return render(request, 'livefeed/live_camera.html', context={
        "cameras": Cameras.objects.all(),
        "camera": camera
    })


@gzip.gzip_page
@require_GET
def video_feed(request, camera_id):

    with open(os.path.join(settings.MEDIA_ROOT, 'representations.pkl') , 'rb') as f:
        representations = pickle.load(f)

    cam = Cameras.objects.filter(id=camera_id).first()
    connection_string = cam.connection_string
    if connection_string == '0':
        connection_string = int(connection_string)
    camera = cv2.VideoCapture(connection_string)
    cameras.append({"id": cam.id, "camera": camera})

    def generate():
        while True:
            ret, frame = camera.read()

            if not ret:
                break

            # Save the frame as an image temporarily
            temp_img_name = "temp_frame.jpg"
            temp_img_path = os.path.join(settings.MEDIA_ROOT, temp_img_name)
            cv2.imwrite(temp_img_path, frame)
            try:
                # Perform facial recognition using DeepFace
                target_faces = DeepFace.extract_faces(img_path=temp_img_path)
                #print(len(target_faces))
                matched_names_all=[]
                if len(target_faces) > 0:
                        print("face: ", len(target_faces))
                        target_representation = DeepFace.represent(img_path=temp_img_path, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]

                        # load representations of faces in database
                        
                        

                        distances = []
                        for i in range(0, len(representations)):
                            source_name = representations[i][0]
                            source_representation = representations[i][1]
                            distance = dst.findCosineDistance(source_representation, target_representation)
                            distances.append(distance)
                    
                        # Find the minimum distance index
                        idx = np.argmin(distances)
                        min_distance = distances[idx]
                        print(min_distance)
                        # Check if the minimum distance is below a certain threshold (adjust threshold as needed)
                        threshold = 0.5
                        if min_distance <= threshold:
                            matched_name = representations[idx][0]
                            detect_person(representations[idx][2],camera_id)

                            print("Matched Name:", matched_name)
                        else:
                            matched_name = "Unknown"
                            detect_unknown(temp_img_path,camera_id)
                            print(matched_name)
                        matched_names_all.append(matched_name)
                        #dfs = DeepFace.find(img_path = temp_img_path, db_path = os.path.join(settings.MEDIA_ROOT, 'representations_vgg.pkl')    )
                        

                        # Find the minimum distance index
                        """idx = np.argmin(distances)
                        matched_name = representations[idx][0]
                        print("Matched Name:", matched_name)"""

                    # Remove the temporary image
                    #if os.path.exists(temp_img_path):
                    #    os.remove(temp_img_path)
            except Exception as e:
                print(f"An exception occurred: {e}")
    
                pass
            ret, jpeg = cv2.imencode('.jpg', frame)
            data = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')