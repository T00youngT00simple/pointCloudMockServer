

if __name__ == "__main__":
    import sys
    import os

    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_DIR  not in sys.path:
        sys.path.insert(0, PROJECT_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pointCloudMockServer.settings")

    import django
    django.setup()

    from mock.models import ClassesSetObject, ClassesSet
    from basicObject.classesSet import classesSets


    try:
        classesSetList = []
        classesSetObjectList = []
        for classesSet in classesSets:
            classesSetObj = ClassesSet(setName=classesSet["name"])
            classesSetObj.save()

            for classesSetObject in classesSet["objects"]:
                classesSetObjectList.append(ClassesSetObject(
                    classSet=classesSetObj,
                    label=classesSetObject.get("label"),
                    color=classesSetObject.get("color"),
                    classIndex=classesSetObject.get("classIndex"),
                    mute=classesSetObject.get("mute"),
                    visible=classesSetObject.get("visible"),
                    solo=classesSetObject.get("solo"),
                    red=classesSetObject.get("red"),
                    green=classesSetObject.get("green"),
                    blue=classesSetObject.get("blue"),
                ))

        ClassesSetObject.objects.bulk_create(classesSetObjectList)

    except:
        ClassesSetObject.objects.all().delete()
        ClassesSet.objects.all().delete()