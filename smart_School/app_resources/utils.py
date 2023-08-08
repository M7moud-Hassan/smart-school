from .models import PersonsDetect, Persons, Cameras
from datetime import datetime

cameras = []


def detect_person(person_id, camera_id):
    try:
        camera = Cameras.objects.get(id=camera_id)
        person = Persons.objects.get(id=person_id)
        detected_at = datetime.now().replace(second=0, microsecond=0)

        persons_detect, created = PersonsDetect.objects.get_or_create(
            camera_id=camera,
            person_id=person,
            detected_at=detected_at,
            defaults={'detected_at': detected_at}
        )
    except Exception as e:
        print("errr:=>",e)


def detect_unknown(image_frame, camera_id):
    try:
        created_at = datetime.now().replace(second=0, microsecond=0)
        person, created = Persons.objects.get_or_create(
            image=image_frame,
            created_at=created_at,
            defaults={'created_at': created_at}
        )
        if created:
            PersonsDetect.objects.create(camera_id=Cameras.objects.get(id=camera_id), person_id=person)
    except Exception:
        pass
