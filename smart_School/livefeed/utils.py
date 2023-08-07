from app_resources.models import PersonsDetect
from deepface import DeepFace
from django.conf import settings
import pickle
import os
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
    instance = [person.name, representation, person.id,person.status] #, person.image.url
    print(instance)
    # Save the instance to the 'representations.pkl' file
    pickle_file_path = os.path.join(settings.MEDIA_ROOT, 'representations.pkl')
    try:
        with open(pickle_file_path, "rb") as f:
            representations = pickle.load(f)
    except FileNotFoundError:
        representations = []

    representations.append(instance)

    with open(pickle_file_path, "wb") as f:
        pickle.dump(representations, f)


    print(len(representations))


def image_update_person(person):
    print(person)


def search_by_image_unknown_filter(image_file):
    return PersonsDetect.objects.all()


def search_by_image_black_filter(image_file):
    return PersonsDetect.objects.all()

def search_by_image_white_filter(image_file):
    return PersonsDetect.objects.all()

def search_by_image_known_filter(image_file):
    return PersonsDetect.objects.all()

def search_by_image_all_filter(image_file):
    return PersonsDetect.objects.all()