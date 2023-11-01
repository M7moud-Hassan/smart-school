from io import BytesIO
from .models import PersonsDetect, Persons, Cameras
from datetime import datetime
from PIL import Image
from django.core.files.base import ContentFile
import numpy as np
import threading
import time

cameras = []

object_data = []
ids=[]

ids_lock = threading.Lock()  # Create a lock to ensure thread safety for the 'ids' list

def clear_ids_list():
    global ids
    with ids_lock:
        ids = []  # Clear the 'ids' list
    threading.Timer(30.0, clear_ids_list).start()  # Schedule the function to run again in 30 seconds

clear_ids_list()

def detect_person(national_id,camera_id):
    try:
        camera = Cameras.objects.get(id=camera_id)
        person = Persons.objects.get(id_national=national_id)
        if   not str(camera_id)+""+str(national_id) in ids  :  #True :
            ids.append(str(camera_id)+""+str(national_id))
            object_data.append({
                "id_camera":camera_id,
                "category":'green' if person.status=='whitelist' else 'red',
                "sort":'white' if person.status=='whitelist' else 'black',
                "id_person":person.id,
                "id":person.id_national,
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
    f=Persons.objects.filter(created_at=created_at)
    if  len(f)>0 : #False:
       pass
    else:
        person = Persons.objects.create(
                image=ContentFile(image_data, name='image.jpg'),
                created_at=created_at,
        )
        PersonsDetect.objects.create(
                camera_id=Cameras.objects.get(id=camera_id),
                person_id=person,
                
        )
        object_data.append({
                    "id_camera":camera_id,
                    "category":'yellow',
                    "sort":'',
                    'id':'',
                    "id_person":person.id,
                    "name":'Unkonwn',
                    "img":person.image.url,
                    "des":"description about person"
            })
    