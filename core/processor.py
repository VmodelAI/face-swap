import concurrent.futures
import os
import queue

import cv2
import insightface
import torch

import core.globals
from core.config import get_face
from core.face_enhancer import face_enhancer
from core.utils import rreplace

if os.path.isfile('../inswapper_128.onnx'):
    face_swapper = insightface.model_zoo.get_model('../inswapper_128.onnx', providers=core.globals.providers)
else:
    quit('File "inswapper_128.onnx" does not exist!')


def process_img(source_img, target_path):
    frame = cv2.imread(target_path)
    face = get_face(frame)
    source_face = get_face(cv2.imread(source_img))
    result = face_swapper.get(frame, face, source_face, paste_back=True)
    target_path = rreplace(target_path, "/", "/swapped-", 1) if "/" in target_path else "swapped-" + target_path
    print(target_path)
    cv2.imwrite(target_path, result)
    return target_path
