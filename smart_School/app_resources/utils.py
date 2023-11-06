from io import BytesIO
from .models import PersonsDetect, Persons, Cameras
from django.utils import timezone
from PIL import Image
from django.core.files.base import ContentFile

cameras = []
object_data = []
ids=[]
def detect_person(national_id,camera_id):
    try:
        camera = Cameras.objects.get(id=camera_id)
        person = Persons.objects.get(id_national=national_id)
        exist=None
        for obj in ids:
            if obj['camera_id']==camera_id and national_id in obj['persons']:
                exist=obj
                break
        if  exist is None:
            for obj in ids:
                if obj['camera_id']==camera_id:
                    obj['persons'].append(national_id)
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
            if camera.camera_type=='outdoor':
                person=PersonsDetect.objects.filter(person_id=person,camera_id__camera_type='indoor').last()
                if person:
                    person.camera_id=camera
                person.save()
            else:
                PersonsDetect.objects.create(
                camera_id=camera,
                person_id=person,
            )
           
    except Exception as e:
        print("errr:=>",e)


def detect_unknown(image_frame, camera_id):
    created_at = timezone.now().replace(second=0, microsecond=0)
    pil_image = Image.fromarray(image_frame)
    image_buffer = BytesIO()
    pil_image.save(image_buffer, format='JPEG')
    image_data = image_buffer.getvalue()
    f=Persons.objects.filter(created_at=created_at)
    if  len(f)>0 :
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
    