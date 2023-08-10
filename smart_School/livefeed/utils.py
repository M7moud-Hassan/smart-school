from app_resources.models import PersonsDetect,Persons
from deepface import DeepFace
from django.conf import settings
import pickle
import os
from deepface.commons import functions, realtime, distance as dst
import pickle
import numpy as np
import os
import cv2
object_data = [
    {
        "id_camera": "5",
        "category": "1,4",
        "sort": "white",
        "id_person": "1",
        "name": "mahmoud",
        "img": "/media/persons/ae0e11e897def7d83f973e029a7d7340.png",
        "des": "mahmoud hassan ahmed",
    },
]


def image_of_person(person):
    print(person)

    # Assuming the 'person' parameter is a Persons model object

    # Calculate the face representation for the person's image
    image_path = person.image.path
    representation = DeepFace.represent(img_path=image_path, model_name="VGG-Face")[0]["embedding"]

    # Create an instance list containing the person's name, representation, and image URL
    instance = [person.name, representation, person.id, person.status]  # , person.image.url

    pickle_file_path = os.path.join(settings.MEDIA_ROOT, 'representations.pkl')

    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, "rb") as f:
            representations = pickle.load(f)
    else:
        representations = []

    representations.append(instance)

    with open(pickle_file_path, "wb") as f:
        pickle.dump(representations, f)

    print(len(representations))






def image_update_person(person):
    print(person)

    # Assuming the 'person' parameter is a Persons model object

    # Calculate the face representation for the person's image
    image_path = person.image.path
    representation = DeepFace.represent(img_path=image_path, model_name="VGG-Face")[0]["embedding"]

    # Create an instance list containing the person's name, representation, ID, and status
    instance = [person.name, representation, person.id, person.status]

    # Load existing representations from 'representations.pkl' if it exists
    pickle_file_path = os.path.join(settings.MEDIA_ROOT, 'representations.pkl')
    try:
        with open(pickle_file_path, "rb") as f:
            representations = pickle.load(f)
    except FileNotFoundError:
        representations = []

    # Find and update the instance for the current person (if it already exists)
    for i, existing_instance in enumerate(representations):
        if existing_instance[2] == person.id:  # Assuming the ID is unique for each person
            representations[i] = instance
            break
    else:
        # If the person's instance doesn't exist in the list, append it
        representations.append(instance)

    # Save the updated or new instance list to the 'representations.pkl' file
    with open(pickle_file_path, "wb") as f:
        pickle.dump(representations, f)

    print(len(representations))



def search_by_image_unknown_filter(image_file):
    
    return PersonsDetect.objects.all()


def search_by_image_black_filter(image_file):
    return PersonsDetect.objects.all()

def search_by_image_white_filter(image_file):
    return PersonsDetect.objects.all()

def search_by_image_known_filter(image_file):
    return PersonsDetect.objects.all()

"""def search_by_image_all_filter(image_file):
    with open(os.path.join(settings.MEDIA_ROOT, 'representations.pkl') , 'rb') as f:
        representations = pickle.load(f)
    # Save the frame as an image temporarily
    print("//////////////////////////////////////////////////",image_file)
    print("image_file.name:", image_file.name)
    print("image_file.size:", image_file.size)
    print("image_file.content_type:", image_file.content_type)
    print(image_file.path)
    temp_img_name = image_file.name
    temp_img_path = os.path.join(settings.MEDIA_ROOT, temp_img_name)
    cv2.imwrite(temp_img_path, temp_img_name)
            #try:
                # Perform facial recognition using DeepFace
    target_faces = DeepFace.extract_faces(img_path=temp_img_path, enforce_detection=False)
            #print(len(target_faces))
    matched_names_all=[]
    if len(target_faces) > 0:
                    
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
                #detect_person(representations[idx][2],camera_id)

                print("Matched Name:", matched_name)
            else:
                matched_name = "Unknown"
                #detect_unknown(temp_img_path,camera_id)
                print(matched_name)
                matched_names_all.append(matched_name)   
    return PersonsDetect.objects.all()

"""
from django.core.files.storage import FileSystemStorage

def search_by_image_all_filter(image_file):
    return PersonsDetect.objects.all()
   