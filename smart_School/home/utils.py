from datetime import datetime,timedelta

from django.forms import model_to_dict
from app_resources.models import PersonsDetect
from config.models import Config, Nabatshieh


def perform_detection(detected_today):
    result=[]
    time_work='08:00:00'
    config=Config.objects.all().first()
    nabatshieh=Nabatshieh.objects.all()
    if config:
        time_work=config.time_end_working()
    for person in detected_today:
        for n in nabatshieh:
            # print(n.persions.all())
            if person.person_id in n.persions.all():
                time_start = datetime.combine(datetime.today(), n.time_start_working)
                time_end = datetime.combine(datetime.today(), n.time_end_working)
                time_work = str(time_end - time_start)
                if ',' in time_work:
                    time_work=time_work.split(',')[1].strip()
        if person.reason is None and person.spend_time:
            if difference_time(person.spend_time,time_work):
                person_dict = model_to_dict(person)
                person_dict['color'] = 'green'
                person_dict['name']=person.person_id.name
                person_dict['reason_in']="لا يوجد"
                person_dict['reason_out']="لا يوجد"
                result.append(person_dict)
            else:
                person_dict = model_to_dict(person)
                person_dict['color'] = 'red'
                person_dict['name']=person.person_id.name
                person_dict['reason_in']="لا يوجد"
                person_dict['reason_out']="لا يوجد"
                result.append(person_dict)
        elif person.reason is None and person.spend_time is None:
            person_dict = model_to_dict(person)
            person_dict['name']=person.person_id.name
            person_dict['reason_in']="لا يوجد"
            person_dict['reason_out']="لا يوجد"
            result.append(person_dict)
        elif person.reason and person.spend_time:
            person_dict = model_to_dict(person)
            person_dict['color']='blue'
            person_dict['name']=person.person_id.name
            person_dict['reason_in']="لا يوجد"
            person_dict['reason_out']=person.reason.reason.name
            result.append(person_dict)
        elif person.reason and person.spend_time is None:
            person_dict = model_to_dict(person)
            person_dict['color']='yellow'
            person_dict['name']=person.person_id.name
            person_dict['reason_out']="لا يوجد"
            person_dict['reason_in']=person.reason.reason.name
            result.append(person_dict)
    return result


def difference_time(spend_time_str,max_time_str):
    spend_time = datetime.strptime(spend_time_str, "%H:%M:%S").time()
    max_time = datetime.strptime(max_time_str, "%H:%M:%S").time()
    time_difference = timedelta(
        hours=spend_time.hour,
        minutes=spend_time.minute,
        seconds=spend_time.second
    )
    time_working=timedelta(
        hours=max_time.hour,
        minutes=max_time.minute,
        seconds=max_time.second
    )
    return time_difference >= time_working