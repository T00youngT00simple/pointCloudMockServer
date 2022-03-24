
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
    header = models.CharField(max_length=512, null=True)

    rotationX = models.IntegerField(default=0)
    rotationY = models.IntegerField(default=0)
    rotationZ = models.IntegerField(default=0)

    # foreignKey model fileHeader
    # save as str  json.dumps(tagList)
    tags = models.CharField(max_length=256, null=True)


class ImageInfo(models.Model):
    filePath = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    sample = models.ForeignKey(Sample, related_name="image", on_delete=models.CASCADE, null=True)


class CloudData(models.Model):
    image = models.ForeignKey(ImageInfo, related_name="imageCloudData", on_delete=models.CASCADE)
    labelName = models.CharField(max_length=256)
    pointIndex = models.CharField(max_length=256)

