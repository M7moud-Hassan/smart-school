import asyncio
from io import BytesIO
import os
from .models import PersonsDetect, Persons, Cameras
from django.utils import timezone
from PIL import Image
from django.core.files.base import ContentFile
import cv2
cameras = []
object_data = []
ids=[]
def detect_person(national_id,camera_id,top, right, bottom, left,frame):
    try:
        camera = Cameras.objects.get(id=camera_id)
        person = Persons.objects.get(id_national=national_id)
        save_image(national_id, frame)
        exist=None
        for obj in ids:
            if obj['camera_id']==camera_id and national_id in obj['persons']:
                exist=obj
                break
        if  exist is None:
            for obj in ids:
                if obj['camera_id']==camera_id:
                    obj['persons'].append(national_id)
            detect=None
            if camera.camera_type=='outdoor':
                detect=PersonsDetect.objects.filter(person_id=person,camera_id__camera_type='indoor').last()
                if detect:
                    detect.camera_id=camera
                    detect.save()
                else:
                    detect=PersonsDetect.objects.create(
                    camera_id=camera,
                    person_id=person,
                )
            else:
                detect=PersonsDetect.objects.create(
                camera_id=camera,
                person_id=person,
            )
            object_data.append({
                "id_camera":camera_id,
                "category":'green' if person.status=='whitelist' else 'red',
                "sort":'white' if person.status=='whitelist' else 'black',
                "id_person":person.id,
                "id":person.id_national,
                "name":person.name,
                "img":person.image.url,
                "des":detect.id
            })
    
        color =(0, 255, 0) if person.status=='whitelist' else (55, 55, 255)
        x, y, w, h = left, top, right - left, bottom - top
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y),color, -1)
        font_size = 0.5
        font_thickness = 1
        font = cv2.FONT_HERSHEY_COMPLEX 
        text_size = cv2.getTextSize(person.name.split(' ')[0], font, font_size, font_thickness)[0]
        text_x = int((w - text_size[0]) / 2) + x
        text_y = y - 15
        cv2.putText(frame, person.name.split(' ')[0], (text_x, text_y), font, font_size, (255, 255, 255), font_thickness)
 
    except Exception as e:
        print("errr:=>",e)


def detect_unknown(top, right, bottom, left,frame):
    #created_at = timezone.now().replace(second=0, microsecond=0)
    #pil_image = Image.fromarray(image_frame)
    #image_buffer = BytesIO()
    #pil_image.save(image_buffer, format='JPEG')
    #image_data = image_buffer.getvalue()
    #f=Persons.objects.filter(created_at=created_at)
    #if  len(f)>0 :
    #   pass
    #else:
    #    person = Persons.objects.create(
    #            image=ContentFile(image_data, name='image.jpg'),
    #            created_at=created_at,
    #    )
    #    PersonsDetect.objects.create(
    #            camera_id=Cameras.objects.get(id=camera_id),
    #            person_id=person,
    #            
    #    )
    #    object_data.append({
    
    #                "id_camera":camera_id,
    #                "category":'yellow',
    #                "sort":'',
    #                'id':'',
    #                "id_person":person.id,
    #                "name":'Unkonwn',
    #                "img":person.image.url,
    #                "des":"description about person"
    #        })
    x, y, w, h = left, top, right - left, bottom - top
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 1)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
    cv2.rectangle(frame, (x, y-40), (x+w, y), (0, 255, 255), -1)
    font_size = 0.5
    font_thickness = 1
    font = cv2.FONT_HERSHEY_COMPLEX 
    text_size = cv2.getTextSize('unknown', font, font_size, font_thickness)[0]
    text_x = int((w - text_size[0]) / 2) + x
    text_y = y - 15
    cv2.putText(frame,'unknown', (text_x, text_y), font, font_size, (255, 255, 255), font_thickness)


def save_image(id,frame):
    folder_path = os.path.join('media/detections', id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    existing_items = len(os.listdir(folder_path))
    image_filename = f"{existing_items + 1}.jpg"
    image_path = os.path.join(folder_path, image_filename)
    pil_image = Image.fromarray(frame)
    pil_image.save(image_path)