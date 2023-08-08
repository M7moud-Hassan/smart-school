from app_resources.models import PersonsDetect

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
