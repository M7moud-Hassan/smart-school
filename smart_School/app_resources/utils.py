from io import BytesIO
from .models import PersonsDetect, Persons, Cameras
from datetime import datetime
from PIL import Image
from django.core.files.base import ContentFile
import numpy as np
cameras = []

object_data = []

def detect_person(national_id,camera_id):
    try:
        camera = Cameras.objects.get(id=camera_id)
        person = Persons.objects.get(id_national=national_id)
        
        object_data.append({
            "id_camera":camera_id,
            "category":'success' if person.status=='whitelist' else 'danger',
            "sort":'white' if person.status=='whitelist' else 'black',
            "id_person":person.id,
            "name":person.name,
            "img":person.image.url,
            "des":"description about person"
        })
        detected_at = datetime.now().replace(second=0, microsecond=0)
        created, p = PersonsDetect.objects.get_or_create(
            camera_id=camera,
            person_id=person,
            detected_at=detected_at,
            defaults={'detected_at': detected_at}
        )
        if camera.camera_type=='outdoor' and created:
            person=PersonsDetect.objects.filter(person_id=person,camera_id__camera_type='indoor').last()
            if person:
                person.spend_time=created.spend_time
                person.outed_at=created.outed_at
                person.save()
                created.detected_at=person.detected_at
                created.save()
            return
    except Exception as e:
        print("errr:=>",e)


def detect_unknown(image_frame, camera_id):
    created_at = datetime.now().replace(second=0, microsecond=0)
    pil_image = Image.fromarray(image_frame)
    image_buffer = BytesIO()
    pil_image.save(image_buffer, format='JPEG')
    image_data = image_buffer.getvalue()
    person = Persons.objects.create(
        image=ContentFile(image_data, name='image.jpg'),
        created_at=created_at
    )
    print('add')
    object_data.append({
            "id_camera":camera_id,
            "category":'warning',
            "sort":'unknown',
            "id_person":person.id,
            "name":person.name,
            "img":person.image.url,
            "des":"description about person"
        })
    PersonsDetect.objects.create(
        camera_id=Cameras.objects.get(id=camera_id),
        person_id=person
    )