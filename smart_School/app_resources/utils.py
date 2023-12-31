
import os

import numpy as np
import requests

from config.models import Config
from .models import PersonsDetect, Persons, Cameras
from PIL import Image
import cv2
import arabic_reshaper 
from bidi.algorithm import get_display 
from PIL import Image, ImageFont, ImageDraw 
cameras = []
object_data = []
ids=[]

def detect_person(national_id,camera_id,top, right, bottom, left,frame):
    try:
        camera = Cameras.objects.get(id=camera_id)
        person = Persons.objects.get(id_national=national_id)
        #save_image(national_id, frame)
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
            sendWhatsAppMessage(person)
        color =(114, 165, 59) if person.status=='whitelist' else (55, 55, 255)
        return draw_name(top, right, bottom, left,frame,person.name,person.department.name,color)
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
   return draw_name(top, right, bottom, left,frame,'غير معروف','',(127,255,255))

def save_image(id,frame):
    folder_path = os.path.join('media/detections', id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    existing_items = len(os.listdir(folder_path))
    image_filename = f"{existing_items + 1}.jpg"
    image_path = os.path.join(folder_path, image_filename)
    pil_image = Image.fromarray(frame)
    pil_image.save(image_path)


def draw_name(top, right, bottom, left,frame,text,dep,color):
    x, y, w, h = left, top, right - left, bottom - top
    draw_border(frame,(left,top),(right,bottom),color,2,5,10)
    rect_color = (128, 128, 128)  
    rect_opacity = 0.5
    overlay = frame.copy()
    cv2.rectangle(overlay, (x+w+100, y-20), (x+w+10, y+20), rect_color, -1)
    cv2.addWeighted(overlay, rect_opacity, frame, 1 - rect_opacity, 0, frame)
    font = cv2.FONT_HERSHEY_COMPLEX 
    reshaped_text = arabic_reshaper.reshape(text)
    reshaped_text2 = arabic_reshaper.reshape(dep)
    bidi_text = get_display(reshaped_text) 
    bidi_text2 = get_display(reshaped_text2) 
    font = ImageFont.truetype("sahel.ttf", size=13)
    im=Image.fromarray(frame)
    d = ImageDraw.Draw(im)
    d.multiline_text((x+w+20,y-20), bidi_text, font=font, spacing=15, align="center")
    d.multiline_text((x+w+20,y), bidi_text2, font=font, spacing=15, align="center")
    return np.array(im)

def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


def sendWhatsAppMessage(person):
    config=Config.objects.all().first()
    if config:
        access_token = config.token_access
        url = config.url_whatsapp
        message_data = {
        "messaging_product": "whatsapp",
        "to": f"2${person.mobile_whatsapp}",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {"code": "en_US"}
        }
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=message_data, headers=headers)

