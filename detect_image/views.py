from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.files.temp import NamedTemporaryFile

import io
import os
from imageio import imwrite
from PIL import Image
import numpy as np
from base64 import b64decode, b64encode
from .utils import *
from .darknet import Darknet
import cv2

# Create your views here.
#########################

@csrf_exempt
def yolo_detect_api(request):
    data = {'success':False}

    if request.method == "POST":

        if request.FILES.get("image", None) is not None:
            image_request = request.FILES["image"]
            image_bytes = image_request.read()
            image = Image.open(io.BytesIO(image_bytes))
            imwrite('temp.png', image)

        elif request.POST.get("image64", None) is not None:
            base64_data = request.POST.get("image64", None).split(',', 1)[1]
            plain_data = b64decode(base64_data)
            plain_data = np.array(Image.open(io.BytesIO(plain_data))) 
            imwrite('temp.png', plain_data)

        result = yolo_detect('temp.png')
        
        if result:
            data['success'] = True

    data['objects'] = result

    return JsonResponse(data)


def detect(request):
    return render(request, 'index.html')

def yolo_detect(image):
    cfg_file = './cfg/yolov3.cfg'

    weight_file = './weights/yolov3.weights'

    namesfile = 'data/coco.names'

    m = Darknet(cfg_file)

    m.load_weights(weight_file)

    class_names = load_class_names(namesfile)

    img = cv2.imread(image)

    original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    resized_image = cv2.resize(original_image, (m.width, m.height))

    nms_thresh = 0.6

    iou_thresh = 0.4

    boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)

    plot_boxes(original_image, boxes, class_names, plot_labels = True)

    return print_objects(boxes, class_names)
