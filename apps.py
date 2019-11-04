from django.apps import AppConfig
import numpy as np # To work with arrays
import cv2
from django.urls import path, include



class BackgroundConfig(AppConfig):
    name = 'background'
    #MODEL_PATH = path("model")
    #BERT_PRETRAINED_PATH = path("model/uncased_L-12_H-768_A-12/")
    #ABEL_PATH = Path("label/")
    #predictor = background.get_colors(get_image('img'), 5)
#get_colors(get_image('sample_image.jpg'), 5)

#BertClassificationPredictor(model_path = MODEL_PATH/"multilabel-emotion-color-suggestion.bin", 
                                            #pretrained_path = BERT_PRETRAINED_PATH, 
                                            #label_path = LABEL_PATH, multi_label=True)