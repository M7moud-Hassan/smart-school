import cv2 
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
from django.views.decorators.http import require_GET
from app_resources.models import *
from app_resources.utils import cameras, detect_person, detect_unknown
from django.conf import settings
import cv2
import os
import os.path
import pickle
import numpy as np
from imutils.video import VideoStream
import imutils
import face_recognition
from django.conf import settings
from app_resources.utils import ids
from config.models import Reasons
from app_resources.views import release_resources
from app_resources.utils import object_data


def all_cameras(request):
    camears_lisy = Cameras.objects.all()
    return render(request, 'livefeed/all.html', context={
        "title": "View Cameras",
        "sub_title": "All",
        "cameras": camears_lisy
    })


def open_camera(request, id):
    release_resources(request)
    camera = Cameras.objects.filter(id=id).first()
    return render(request, 'livefeed/live_camera.html', context={
        "cameras": Cameras.objects.all(),
        "camera": camera,
        'reasons':Reasons.objects.filter(when='الدخول' if camera.camera_type=='indoor' else 'الخروج')
    })

####################################################### 
MODEL =  "hog"  #hog "cnn"
TOLERANCE = 0.55 
######################################################


# Global variable to keep track of frame skipping counters for each recognized person
skip_frames_counter = {}

# Define how many frames to skip after detecting a person
FRAMES_TO_SKIP = 30


camera=None
@gzip.gzip_page
@require_GET
def video_feed(request, camera_id):
    global ids
    exists=False
    for obj in ids:
         if obj['camera_id']==camera_id:
              obj['persons'].clear()
              exists=True
              break
    
    if not exists:
         ids.append({
              "camera_id":camera_id,
              "persons":[]
         })
    # with open(os.path.join(settings.MEDIA_ROOT, 'representations.pkl') , 'rb') as f:
    #     representations = pickle.load(f)
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

    def generate():
            while True:
                frame = camera.read()
                #frame = imutils.resize(frame, WIDTH_SCALE = 320)
                if camera is None:
                     break
                if frame is None:
                    continue
                try:
                     #frame = imutils.resize(frame, width=600, height=600)
                    
                    #rgb_frame  =np.ascontiguousarray(frame[:, :, ::-1]) #frame[:, :, ::-1] #frame#[:, :, ::-1]
                    
                    #face_locations = face_recognition.face_locations(rgb_frame, model = MODEL )#))
                    #frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)
                    frame = imutils.resize(frame, width=320, height=320)
                    
                    #rgb_frame  = np.ascontiguousarray(frame[:, :, ::-1]) #frame[:, :, ::-1] #frame#[:, :, ::-1]
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    face_locations = face_recognition.face_locations(rgb_frame,model = MODEL )#))number_of_times_to_upsample=2,number_of_times_to_upsample=1
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    

                    name = []
                    #print("Numbr of faces:", len(face_encodings))
                    # Loop through each face found in the unknown image
                    if len(face_encodings)<5:
                        #for face_encoding in  face_encodings:
                        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                            # See if the face is a match for the known face(s)
                            matches = face_recognition.compare_faces(settings.KNOW_FACE_ENCODINGS, face_encoding,tolerance=TOLERANCE)

                            

                            # Or instead, use the known face with the smallest distance to the new face
                            face_distances = face_recognition.face_distance(settings.KNOW_FACE_ENCODINGS, face_encoding)
<<<<<<< HEAD
=======
                            #################################
>>>>>>> d087f4c123a422e34a215914c15bf27115152fd0

                            min_distance = min(face_distances)
                            best_match_index = np.argmin(face_distances)
                            match_percentage = face_distances[best_match_index] / TOLERANCE
                            match_percentage = match_percentage * 100
<<<<<<< HEAD
                            match_percentage = "%" + str("{:.2f}".format(match_percentage))

                            print(min_distance , match_percentage)
                            if min_distance <= 0.2:
                                best_match_index = np.argmin(face_distances)
                                if matches[best_match_index]:
                                    name.append(settings.KNOW_FACE_NAMES[best_match_index])
                                
                                if matches[best_match_index] :
                                    print(settings.KNOW_FACE_NAMES[best_match_index])
                                    if "_"in settings.KNOW_FACE_NAMES[best_match_index]:
                                        # Check if we should skip frames for this recognized person
                                        #f skip_frames_counter.get(settings.KNOW_FACE_NAMES[best_match_index].split("_")[0], 0) > 0:
                                            # Reduce the counter for this person and skip the detection
                                        #    skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index].split("_")[0]] -= 1
                                    # else:
                                            # Detect the person and reset the skip counter
                                        detect_person(settings.KNOW_FACE_NAMES[best_match_index].split("_")[0],camera_id)

                                    #     skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index].split("_")[0]] = FRAMES_TO_SKIP
                                        
                                    else:

=======
                            match_percentage = "%" + str("{:.2f}".format(match_percentage)) 
                            print(min_distance , match_percentage)
                            if min_distance <= 0.4:
                            #######################################
                                best_match_index = np.argmin(face_distances)
                                if matches[best_match_index]:
                                    name.append(settings.KNOW_FACE_NAMES[best_match_index])
                                
                                if matches[best_match_index] :
                                    print(settings.KNOW_FACE_NAMES[best_match_index])
                                    if "_"in settings.KNOW_FACE_NAMES[best_match_index]:
                                        # Check if we should skip frames for this recognized person
                                        #f skip_frames_counter.get(settings.KNOW_FACE_NAMES[best_match_index].split("_")[0], 0) > 0:
                                            # Reduce the counter for this person and skip the detection
                                        #    skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index].split("_")[0]] -= 1
                                    # else:
                                            # Detect the person and reset the skip counter
                                        #detect_person(settings.KNOW_FACE_NAMES[best_match_index].split("_")[0],camera_id)
                                        detect_person(settings.KNOW_FACE_NAMES[best_match_index].split("_")[0],camera_id,top, right, bottom, left,frame)
                                    #     skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index].split("_")[0]] = FRAMES_TO_SKIP
                                        
                                    else:

>>>>>>> d087f4c123a422e34a215914c15bf27115152fd0
                                        # Check if we should skip frames for this recognized person
                                        #if skip_frames_counter.get(settings.KNOW_FACE_NAMES[best_match_index], 0) > 0:
                                            # Reduce the counter for this person and skip the detection
                                        #    skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index]] -= 1
                                    # else:
                                            # Detect the person and reset the skip counter
<<<<<<< HEAD
                                        detect_person(settings.KNOW_FACE_NAMES[best_match_index],camera_id)

                                        #    skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index]] = FRAMES_TO_SKIP
                                        #detect_person(settings.KNOW_FACE_NAMES[best_match_index],camera_id)
                                    print("////////////////////////////////////////////")
                                else:
                                    #detect_unknown(frame,camera_id)
                                    print("unknow !!!!!!!!!!!!!!!!!!!!!")
                            else:
                                print("unknow !!!!!!!!!!!!!!!!!!!!!")
=======
                                         detect_person(settings.KNOW_FACE_NAMES[best_match_index],camera_id,top, right, bottom, left,frame)

                                        #    skip_frames_counter[settings.KNOW_FACE_NAMES[best_match_index]] = FRAMES_TO_SKIP
                                        #detect_person(settings.KNOW_FACE_NAMES[best_match_index],camera_id)
                                    ##print("////////////////////////////////////////////")
                                else:
                                    frame=detect_unknown(top, right, bottom, left,frame)
                                    print("unknow !!!!!!!!!!!!!!!!!!!!!")
                            else:
                                frame=detect_unknown(top, right, bottom, left,frame)
                                print("unknow !!!!!!!!!!!!!!!!!!!!!")

                    
>>>>>>> d087f4c123a422e34a215914c15bf27115152fd0
                except Exception as e:
                        print(f"An exception occurred: {e}")
                _, jpeg = cv2.imencode('.jpg', frame)
                data = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

    # Load a sample picture and learn how to recognize it.
    #  mahmoud_image = face_recognition.load_image_file(os.path.join(settings.MEDIA_ROOT, 'persons', 'whitelist', '207200126_163023945858962_4456991363376213271_n.jpg'))
    # mahmoud_face_encoding = face_recognition.face_encodings(mahmoud_image)[0]

    # Load a second sample picture and learn how to recognize it.
    # nada_image = face_recognition.load_image_file(os.path.join(settings.MEDIA_ROOT, 'persons', 'whitelist', 'face2.PNG'))
    # biden_face_encoding = face_recognition.face_encodings(nada_image)[0]

    # Create arrays of known face encodings and their names
    # known_face_encodings = [
    #    mahmoud_face_encoding,
    #    biden_face_encoding
    # ]
    # known_face_names = [
    #     "Mahmoud",
    #     "Nada"
    # ]

    # Initialize some variables
    # face_locations = []
    # face_encodings = []
    # face_names = []
    # process_this_frame = 29
    # i = 0

    # while True:
    #     ret, frame = camera.read()
    #
    #     if not ret:
    #         break
    #     """img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    #     process_this_frame = process_this_frame + 1
    #     if process_this_frame % 30 == 0:
    #         predictions = predict(img, model_path=os.path.join(settings.MEDIA_ROOT, "trained_knn_model.clf") )
    #     frame = show_prediction_labels_on_image(frame, predictions)"""
    # cv2.imshow('camera', frame)

    # Save the frame as an image temporarily
    # """temp_img_name = "temp_frame.jpg"
    # temp_img_path = os.path.join(settings.MEDIA_ROOT, temp_img_name)
    # cv2.imwrite(temp_img_path, frame)"""

    # """process_this_frame = process_this_frame + 1
    # if process_this_frame % 30 == 0:
    #     # Resize frame of video to 1/4 size for faster face recognition processing
    #     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #
    #     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    #     rgb_small_frame = small_frame[:, :, ::-1]
    #
    #     # Find all the faces and face encodings in the current frame of video
    #     face_locations = face_recognition.face_locations(rgb_small_frame)
    #     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    #
    #     face_names = []
    #     for face_encoding in face_encodings:
    #         # See if the face is a match for the known face(s)
    #         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    #         name = "Unknown"
    #
    #         # # If a match was found in known_face_encodings, just use the first one.
    #         # if True in matches:
    #         #     first_match_index = matches.index(True)
    #         #     name = known_face_names[first_match_index]
    #
    #         # Or instead, use the known face with the smallest distance to the new face
    #         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    #         best_match_index = np.argmin(face_distances)
    #         if matches[best_match_index]:
    #             name = known_face_names[best_match_index]
    #
    #         face_names.append(name)
    #
    # #process_this_frame = not process_this_frame
    #
    #
    # # Display the results
    # for (top, right, bottom, left), name in zip(face_locations, face_names):
    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    #     top *= 4
    #     right *= 4
    #     bottom *= 4
    #     left *= 4
    #
    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    #
    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)"""
    #####################################################################################################################################deep face###################################
    # try:
    #
    #     # Perform facial recognition using DeepFace
    #
    #     i =i+1
    #     if i % 30 == 0:
    #         frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #         target_faces = DeepFace.extract_faces(frame)
    #         if len(target_faces) > 0:
    #                 print("face: ", len(target_faces))
    #                 target_representation = DeepFace.represent(frame, model_name="VGG-Face", enforce_detection=False, detector_backend="ssd", align=True)[0]["embedding"]
    #
    #                 # load representations of faces in database
    #                 distances = []
    #                 for i in range(0, len(representations)):
    #                     source_representation = representations[i][1]
    #                     distance = dst.findCosineDistance(source_representation, target_representation)
    #                     distances.append(distance)
    #
    #                 # Find the minimum distance index
    #                 idx = np.argmin(distances)
    #                 min_distance = distances[idx]
    #                 print(min_distance)
    #                 # Check if the minimum distance is below a certain threshold (adjust threshold as needed)
    #                 threshold = 0.5
    #                 if min_distance <= threshold:
    #                     matched_name = representations[idx][0]
    #                     detect_person(representations[idx][2],camera_id)
    #
    #                     print("Matched Name:", matched_name)
    #                 else:
    #                     matched_name = "Unknown"
    #                     detect_unknown(frame,camera_id)
    #         #i = i+1
    # except Exception as e:
    #     print(f"An exception occurred: {e}")
    #
    #     pass
    #         ret, jpeg = cv2.imencode('.jpg', frame)
    #         data = jpeg.tobytes()
    #         yield (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')
    #
    # return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')