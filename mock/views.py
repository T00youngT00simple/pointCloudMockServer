
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from toolset.apilnlines import extractApiKwargs
from django.utils.translation import ugettext as _

from .models import ImageInfo, CloudData, Sample
import json

class cloudData(APIView):
    # if cloudData:
    #     cloudData: how to save

    # {  cloudData
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


    def post(self, request, imageId, format=None):
        if not imageId :
            raise ValidationError(_("Image required"))

        kwargs = extractApiKwargs(request.data, ['cloudData'])
        cloudData = kwargs.get('cloudData')
        cloudDataInfoList = []

        imageInfoObj = ImageInfo.objects.get(pk=imageId)

        CloudData.objects.filter(image_id=imageId).delete()

        if cloudData :

            for selectedLabelName, value in cloudData.items():
                for pointIndex in value:
                    cloudDataInfoList.append(CloudData(image=imageInfoObj, labelName=selectedLabelName, pointIndex=pointIndex))

            CloudData.objects.bulk_create(cloudDataInfoList)

        return Response({})


class getImageInfoList(APIView):
    # res from api
    # { imageInfoList
    #  [
    #         {
    #             id: ,
    #             name: "bitmap_labeling.png",
    #             url: "//bitmap_labeling.png",
    #         }, {
    #             id: ,
    #             name: "bitmap_labeling.png",
    #             url: "//bitmap_labeling.png",
    #         }
    #  ]
    # }
    def get(self, request, format=None):
        imageInfoObj = ImageInfo.objects.all()

        if not imageInfoObj:
            return Response({"images": []})
        else:
            imageInfoList = [{
                "id": imageInfo.id,
                "name": imageInfo.name,
                "url": imageInfo.filePath
            } for imageInfo in imageInfoObj]

            return Response({"images": imageInfoList})


class getImageInfoDetail(APIView):
    # { image Details
    #       id: ,
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
    # { samples
    #      "id": "1",
    #      "url": "http:// ....pointcloud_labeling.pcd",
    #      "socName": "Cityscapes",
    #      "header":  {...}   #file.header  json load
    #      "rotationX": 0,
    #      "rotationY": 0,
    #      "rotationZ": 0,
    #      "folder": "",
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
                    "header": sampleObj.header and json.loads(sampleObj.header) or {},
                    "url": imageInfoObj.filePath,
                    "socName": sampleObj.socName,
                    "rotationX": sampleObj.rotationX,
                    "rotationY": sampleObj.rotationY,
                    "rotationZ": sampleObj.rotationZ,
                    "file": imageInfoObj.name,
                    "tags": sampleObj.tags and json.loads(sampleObj.tags) or [],
                }

            return Response({"sample": sampleDic})


    def post(self, request, imageId, format=None):
        if not imageId:
            raise ValidationError(_("Image required"))

        kwargs = extractApiKwargs(request.data, ['header', 'rotationX', 'rotationY', 'rotationZ', 'socName'])
        header = kwargs.get("header")
        socName = kwargs.get("socName")
        rotationX = kwargs.get("rotationX")
        rotationY = kwargs.get("rotationY")
        rotationZ = kwargs.get("rotationZ")

        imageInfoObj = ImageInfo.objects.get(pk=imageId)

        if not imageInfoObj:
            raise ValidationError(_("Dont have this image"))
        else:
            if not imageInfoObj.sample:
                sample = Sample(socName=socName, header=header and json.dumps(header) or None, rotationX=rotationX,
                                rotationY=rotationY, rotationZ=rotationZ,)

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

        return Response({"image": {}})

