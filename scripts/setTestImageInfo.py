

if __name__ == "__main__":
    import sys
    import os

    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_DIR  not in sys.path:
        sys.path.insert(0, PROJECT_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pointCloudMockServer.settings")

    import django
    django.setup()

    from mock.models import ImageInfo


    try:
        imageInfoObj = ImageInfo(filePath="http://36.138.169.88:8090/mnt/shumi-dev2/shumi-dev/file-store/project-resource/tagging_data/123262/POINT_CLOUD-123262-148/pcd-inside-1/000041.pcd", name="000041.pcd")
        imageInfoObj.save()

    except:
        ImageInfo.objects.all().delete()