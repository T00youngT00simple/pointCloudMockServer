
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from toolset.apilnlines import extractApiKwargs
from django.utils.translation import ugettext as _
from django.db import transaction

from .models import ImageInfo, CloudData, Sample, Tag, ClassesSet
import json

class cloudData(APIView):
    # if cloudData:
    #     cloudData: how to save

    # {  //cloudData
    #      "bus": [0, 1, 2, 3, 4, 5, 7, 8, 99, 2323, 45454],
    #      "road": [222, 223, 224, 225, 260, 278, 12332, 412411],
    #      "car": [124512, 433434],
    # },
    def get(self, request, imageId, format=None):
        if not imageId :
            raise ValidationError(_("Image required"))

        cloudDataInfoObjList = CloudData.objects.filter(image_id=imageId).all()
        labelNameList = []

        cloudData = {}

        for cloudDataInfoObj in cloudDataInfoObjList:
            if cloudDataInfoObj.labelName not in labelNameList:
                labelNameList.append(cloudDataInfoObj.labelName)
                cloudData[cloudDataInfoObj.labelName] = []

            else:
                cloudData[cloudDataInfoObj.labelName].append(cloudDataInfoObj.pointIndex)

        return Response({"cloudData": cloudData})


    @transaction.atomic
    def post(self, request, imageId, format=None):
        if not imageId :
            raise ValidationError(_("Image required"))

        kwargs = extractApiKwargs(request.data, ['cloudData'])
        cloudData = kwargs.get('cloudData')
        cloudDataInfoList = []

        imageInfoObj = ImageInfo.objects.get(pk=imageId)

        if cloudData :
            CloudData.objects.filter(image_id=imageId).delete()

            for selectedLabelName, value in cloudData.items():
                for pointIndex in value:
                    cloudDataInfoList.append(CloudData(image=imageInfoObj, labelName=selectedLabelName, pointIndex=pointIndex))

            CloudData.objects.bulk_create(cloudDataInfoList)

        return Response({})


class getImageInfoList(APIView):
    # res from api
    # { //imageInfoList
    #     [
    #         {
    #             id: ,
    #             name: "bitmap_labeling.png",
    #             url: "//bitmap_labeling.png",
    #         }, {
    #             id: ,
    #             name: "bitmap_labeling.png",
    #             url: "//bitmap_labeling.png",
    #         }
    #     ]
    # }
    def get(self, request, format=None):
        imageInfoObjList = ImageInfo.objects.all()

        if not imageInfoObjList:
            return Response({"images": []})
        else:
            imageInfoList = [{
                "id": imageInfo.id,
                "name": imageInfo.name,
                "url": imageInfo.filePath
            } for imageInfo in imageInfoObjList]

            return Response({"images": imageInfoList})


class getImageInfoDetail(APIView):
    # { //imageDetails
    #       id: 1,
    #       name: "bitmap_labeling.png",
    #       url: "//bitmap_labeling.png",
    # },
    def get(self, request, imageId, format=None):
        if not imageId:
            raise ValidationError(_("Image required"))

        imageInfoObj = ImageInfo.objects.get(pk=imageId)

        if not imageInfoObj:
            return Response({"image": {}})
        else:
            imageDic = {
                "id": imageInfoObj.id,
                "name": imageInfoObj.name,
                "url": imageInfoObj.filePath
            }

            return Response({"image": imageDic})


class samples(APIView):
    # { //samples
    #      "id": "1",
    #      "url": "http:// ....pointcloud_labeling.pcd",
    #      "socName": "Cityscapes",
    #      "header":  {...}   #file.header  json load
    #      "rotationX": 0,
    #      "rotationY": 0,
    #      "rotationZ": 0,
    #      "file": "pointcloud_labeling.pcd",
    #      "tags": [
    #           "1",
    #           "dfgdfgdfgdfg"
    #           ]
    # }
    def get(self, request, imageId, format=None):
        if not imageId:
            raise ValidationError(_("Image required"))

        imageInfoObj = ImageInfo.objects.get(pk=imageId)

        if not imageInfoObj:
            raise ValidationError(_("Dont have this image"))
        else:
            if not imageInfoObj.sample:
                return Response({"sample": {}})

            else:
                sampleObj = imageInfoObj.sample

                sampleDic = {
                    "id": sampleObj.id,
                    "imageId": imageInfoObj.id,
                    "header": sampleObj.header and json.loads(sampleObj.header) or {},
                    "url": imageInfoObj.filePath,
                    "socName": sampleObj.socName,
                    "rotationX": sampleObj.rotationX,
                    "rotationY": sampleObj.rotationY,
                    "rotationZ": sampleObj.rotationZ,
                    "file": imageInfoObj.name,
                    "tags": [tagObj and tagObj.tagName or None for tagObj in imageInfoObj.imageTags.all()],
                }

            return Response({"sample": sampleDic})


    @transaction.atomic
    def post(self, request, imageId, format=None):
        if not imageId:
            raise ValidationError(_("Image required"))

        kwargs = extractApiKwargs(request.data, ['header', 'rotationX', 'rotationY', 'rotationZ', 'socName', 'tags'])
        header = kwargs.get("header")
        socName = kwargs.get("socName")
        rotationX = kwargs.get("rotationX")
        rotationY = kwargs.get("rotationY")
        rotationZ = kwargs.get("rotationZ")
        tags = kwargs.get("tags")

        imageInfoObj = ImageInfo.objects.get(pk=imageId)

        if not imageInfoObj:
            raise ValidationError(_("Dont have this image"))
        else:
            if tags:
                allTags = [tagObj.tagName for tagObj in Tag.objects.all()]

                tagObjList = [ Tag(image=imageInfoObj, tagName=tag) for tag in tags if tag not in allTags]
                Tag.objects.bulk_create(tagObjList)

            if not imageInfoObj.sample:
                sample = Sample(socName=socName, header=header and json.dumps(header) or None, rotationX=rotationX,
                                rotationY=rotationY, rotationZ=rotationZ)

                sample.save()
                imageInfoObj.sample = sample
                imageInfoObj.save()

            else:
                sample = imageInfoObj.sample

                if header is not None or socName is not None or rotationY is not None or rotationX is not None \
                        or rotationZ is not None:
                    updatedFields = set()

                    def updateAttr(obj, attr, value):
                        if value is not None and getattr(obj, attr) != value:
                            updatedFields.add(attr)
                            setattr(obj, attr, value)

                    updateAttr(sample, "header", header and json.dumps(header))
                    updateAttr(sample, "socName", socName)
                    updateAttr(sample, "rotationY", rotationY)
                    updateAttr(sample, "rotationX", rotationX)
                    updateAttr(sample, "rotationZ", rotationZ)

                sample.save()

        return Response({"sample": {}})


class tagList(APIView):
    # [ //tags
    #   "1", "sdfs", "sdfsdf"
    # ]
    def get(self, request, format=None):

        tagObjList = Tag.objects.all()

        return Response({"tags": [tagObj.tagName for tagObj in tagObjList ]})


class getClassesSets(APIView):
    # [ //classesSet
    #     {
    #         "name": "Cityscapes",
    #         "objects": [
    #             {
    #                 "label": "VOID",
    #                 "color": "#CFCFCF",
    #                 "classIndex": 0,
    #                 "mute": False,
    #                 "solo": False,
    #                 "visible": True,
    #                 "red": 0.80859375,
    #                 "green": 0.80859375,
    #                 "blue": 0.80859375
    #             }]
    # ]
    def get(self, request, format=None):
        classesSets = [ {
            "name": classesSetObj.setName,
            "objects": [
                {
                    "label": setObejct.label,
                    "color": setObejct.color,
                    "classIndex": setObejct.classIndex,
                    "mute": setObejct.mute,
                    "solo": setObejct.solo,
                    "visible": setObejct.visible,
                    "red": setObejct.red and float(setObejct.red),
                    "green": setObejct.green and float(setObejct.green),
                    "blue": setObejct.blue and float(setObejct.biue),
                }
                for setObejct in classesSetObj.setObject.all() ]
        } for classesSetObj in ClassesSet.objects.all() ]

        return Response({"classesSets": classesSets})

