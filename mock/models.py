
from django.db import models


class Sample(models.Model):
    socName = models.CharField(max_length=128, null=True)
    # foreignKey model fileHeader
    # save as str  json.dumps(headerObj)
    # "header": {
    #     "data": "ascii",
    #     "headerLen": 197,
    #     "str": "\r\nVERSION 0.7\r\nFIELDS x y z intensity\r\nSIZE 4 4 4 4\r\nTYPE F F F F\r\nCOUNT 1 1 1 1\r\nWIDTH 34720\r\nHEIGHT 1\r\nVIEWPOINT 0 0 0 1 0 0 0\r\nPOINTS 34720\r\nDATA ascii\r",
    #     "version": 0.7,
    #     "fields": [
    #         "x",
    #         "y",
    #         "z",
    #         "intensity"
    #     ],
    #     "size": [
    #         4,
    #         4,
    #         4,
    #         4
    #     ],
    #     "type": [
    #         "F",
    #         "F",
    #         "F",
    #         "F"
    #     ],
    #     "count": [
    #         1,
    #         1,
    #         1,
    #         1
    #     ],
    #     "width": 34720,
    #     "height": 1,
    #     "viewpoint": {
    #         "tx": "0",
    #         "ty": "0",
    #         "tz": "0",
    #         "qw": "1",
    #         "qx": "0",
    #         "qy": "0",
    #         "qz": "0"
    #     },
    #     "points": 34720,
    #     "offset": {
    #         "x": 0,
    #         "y": 1,
    #         "z": 2,
    #         "intensity": 3
    #     },
    #     "rowSize": 0
    # },
    header = models.CharField(max_length=770, null=True)

    rotationX = models.IntegerField(default=0)
    rotationY = models.IntegerField(default=0)
    rotationZ = models.IntegerField(default=0)


class ImageInfo(models.Model):
    filePath = models.CharField(max_length=256)
    name = models.CharField(max_length=128)
    sample = models.ForeignKey(Sample, related_name="image", on_delete=models.CASCADE, null=True)


class CloudData(models.Model):
    image = models.ForeignKey(ImageInfo, related_name="imageCloudData", on_delete=models.CASCADE)
    labelName = models.CharField(max_length=128)
    pointIndex = models.IntegerField(null=True)


class ObjectData(models.Model):
    image = models.ForeignKey(ImageInfo, related_name="imageObjectData", on_delete=models.CASCADE)
    classIndex = models.CharField(max_length=64)
    objectId = models.CharField(max_length=64)


class ObjectDataPointIndex(models.Model):
    objectData = models.ForeignKey(ObjectData, related_name="objectDataPointIndex", on_delete=models.CASCADE)
    pointIndex = models.IntegerField(null=True)


class Tag(models.Model):
    image = models.ForeignKey(ImageInfo, related_name="imageTags", on_delete=models.CASCADE, null=True)
    tagName = models.CharField(max_length=128)


class ClassesSet(models.Model):
    setName = models.CharField(max_length=128)


class ClassesSetObject(models.Model):
    classSet =  models.ForeignKey(ClassesSet, related_name="setObject", on_delete=models.CASCADE)
    label = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    classIndex = models.IntegerField(null=True)
    mute = models.BooleanField(null=True)
    solo = models.BooleanField(null=True)
    visible = models.BooleanField(null=True)
    red = models.CharField(max_length=64, null=True)
    green = models.CharField(max_length=64, null=True)
    blue = models.CharField(max_length=64, null=True)
