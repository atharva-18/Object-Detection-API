from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.files.temp import NamedTemporaryFile

import io
import os
from PIL import Image
import cv2
import numpy as np
from base64 import b64decode, b64encode
from .utils import *
from .darknet import Darknet

# Create your views here.
#########################

@csrf_exempt
def yolo_detect_api(request):
    data = {'success':False}
    url = ''

    if request.method == "POST":
        if request.FILES.get("image", None) is not None:
            image_request = request.FILES["image"]
            image_bytes = image_request.read()
            image = Image.open(io.BytesIO(image_bytes))
            result, url = yolo_detect(image)
        elif request.POST.get("image64", None) is not None:
            base64_data = request.POST.get("image64", None).split(',', 1)[1]
            plain_data = b64decode(base64_data)
            plain_data = np.array(Image.open(io.BytesIO(plain_data)))
            result, url = yolo_detect(plain_data)

        if result:
            data['success'] = True

    data['objects'] = result
    data['url'] = url
    return JsonResponse(data)

def detect(request):
    return render(request, 'index.html')

def yolo_detect(original_image):
    cfg_file = './cfg/yolov3.cfg'
    weight_file = './weights/yolov3.weights'
    namesfile = 'data/coco.names'

    m = Darknet(cfg_file)
    m.load_weights(weight_file)
    class_names = load_class_names(namesfile)

    resized_image = cv2.resize(original_image, (m.width, m.height))

    nms_thresh = 0.6
    iou_thresh = 0.4

    boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)
    url = plot_boxes(original_image, boxes, class_names, plot_labels = True)
    objects = print_objects(boxes, class_names)
    return objects, url
