from .models import PersonsDetect, Persons, Cameras

cameras = []


def detect_person(person_id, camera_id):
    PersonsDetect.objects.create(camera_id=Cameras.objects.get(id=camera_id),
                                 person_id=Persons.objects.get(id=person_id))


def detect_unknown(image_frame, camera_id):
    person = Persons.objects.create(
        image=image_frame
    )
    PersonsDetect.objects.create(camera_id=Cameras.objects.get(id=camera_id), person_id=person)

